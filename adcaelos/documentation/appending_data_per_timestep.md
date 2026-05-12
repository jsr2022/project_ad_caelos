# Appending to NumPy Arrays in `Truth_Component.__data_storage`

## The Original Problem

In `adcaelos/components/truth_component.py` (line 159–171), the `store_data` method iterates over a dictionary and appends values to a storage dictionary:

```python
def store_data(self, data) -> None:
    for label, values in data.items():
        if label not in self.__data_storage:
            self.__data_storage[label] = []
        self.__data_storage[label].extend(values)
```

The user asked: **Can this be done in a single line, without an explicit loop?**

Additional constraints were later clarified:

- Keys are strings, values are **NumPy arrays**.
- Each array in `__data_storage` is **huge**: `N_states × potentially trillions of time steps`.
- Each call appends only a **single time step** (one column) to each array.
- **No copying of existing data** is acceptable — the arrays are too large to duplicate.

---

## Why This Is Hard

NumPy `ndarray` objects have a **fixed-size memory buffer**. Any operation that makes an array larger (`np.append`, `np.concatenate`, `np.resize`, etc.) **must allocate a new buffer and copy all existing data** into it. For arrays with trillions of time steps, this copy is prohibitively expensive.

So the real question becomes: **how do we grow per-key storage without ever copying the already-written data?**

Below are four strategies, each with a one-liner (or near-one-liner) update path, followed by a detailed pros/cons analysis.

---

## Option 1: Pre-allocate a Large Enough Buffer

### Concept
Allocate each key's array once at a known maximum size (`max_steps`), then write each new time step directly into the next empty column. No resizing, no copying.

### Initialization (once)
```python
max_steps = 10_000_000  # estimate or over-allocate
self.__data_storage = {
    label: np.empty((n_states, max_steps), dtype=dtype)
    for label, n_states in state_sizes.items()
}
self.__next_col = 0
```

### One-line update
```python
[
    self.__data_storage[label].__setitem__((slice(None), self.__next_col), values)
    for label, values in data.items()
]; self.__next_col += 1
```

### At the end (optional trim — view, not copy)
```python
self.__data_storage = {
    lab: arr[:, :self.__next_col] for lab, arr in self.__data_storage.items()
}
```

### Pros
| Pro | Detail |
|-----|--------|
| **Zero copies of existing data** | Writing into a pre-allocated column is an in-place operation. |
| **True one-liner update** | The entire per-step update is a single expression. |
| **Predictable memory usage** | Total allocation is known up front. |
| **Cache-friendly** | Data is contiguous in memory; no indirection. |

### Cons
| Con | Detail |
|-----|--------|
| **Requires knowing `max_steps`** | If underestimated, you run out of space and must copy (defeating the purpose). |
| **Wastes memory if over-allocated** | Unused columns sit in RAM (or you accept the waste). |
| **All keys share the same step count** | If different keys need different lengths, you need separate counters. |
| **Not resizable** | Cannot grow beyond the pre-allocated size without a full copy. |

---

## Option 2: Chunked List of Fixed-Size Arrays

### Concept
Store each key's data as a **list of chunks** (e.g., 1-million-column arrays). The current chunk has a write pointer. When it fills up, allocate a new chunk. Existing chunks are never moved.

### Initialization (once)
```python
CHUNK = 1_000_000  # columns per chunk
self.__data_storage = {
    label: [np.empty((n_states, CHUNK), dtype=dtype)]
    for label, n_states in state_sizes.items()
}
self.__chunk_pos = {label: 0 for label in self.__data_storage}
```

### Compact update (hard to compress into a safe one-liner — a small loop is clearer)
```python
for label, values in data.items():
    p = self.__chunk_pos[label]
    chunk = self.__data_storage[label][-1]
    if p >= chunk.shape[1]:
        chunk = np.empty((chunk.shape[0], CHUNK), dtype=chunk.dtype)
        self.__data_storage[label].append(chunk)
        self.__chunk_pos[label] = 0
        p = 0
    chunk[:, p] = values
    self.__chunk_pos[label] = p + 1
```

### When you need a single array (rare, at analysis time)
```python
full = np.concatenate(self.__data_storage[label], axis=1)  # one copy, done once
```

### Pros
| Pro | Detail |
|-----|--------|
| **No copying of already-written data** | Each chunk is written once and never moved. |
| **Unbounded growth** | No need to predict total steps; new chunks are allocated on demand. |
| **Per-key flexibility** | Different keys can have different numbers of chunks. |
| **Memory-efficient allocation** | Only one small chunk allocated per overflow event. |

### Cons
| Con | Detail |
|-----|--------|
| **Not a true one-liner** | The update needs a small procedural loop (hard to compress safely). |
| **Indirection overhead** | Final `np.concatenate` is O(total data) when accessed as a single array. |
| **Slightly more complex bookkeeping** | Requires tracking chunk positions per key. |
| **Fragmented memory** | Chunks may be scattered in RAM (minor in practice). |

---

## Option 3: Resizable On-Disk Containers (`h5py` / `zarr`)

### Concept
Store each key as a **resizable HDF5 dataset** (via `h5py`) or a `zarr` array. These formats support `resize()` along an axis without rewriting existing data — the file system handles growth.

### Initialization (once)
```python
import h5py
self.__h5 = h5py.File("sim_data.h5", "w")
self.__dsets = {}
for label, n_states in state_sizes.items():
    self.__dsets[label] = self.__h5.create_dataset(
        label,
        shape=(n_states, 0),
        maxshape=(n_states, None),   # unlimited growth on axis 1
        dtype=dtype,
        chunks=(n_states, CHUNK),
    )
```

### Compact update
```python
for label, values in data.items():
    ds = self.__dsets[label]
    ds.resize(ds.shape[1] + 1, axis=1)
    ds[:, -1] = values
```

### Pros
| Pro | Detail |
|-----|--------|
| **Truly no-copy growth** | `resize()` extends the dataset in-place on disk. |
| **Data exceeds RAM** | Only the active chunk is in memory; rest lives on disk. |
| **Portable, inspectable** | HDF5 files can be opened in MATLAB, Python, Julia, etc. |
| **Compression support** | Built-in gzip/lzf filters reduce disk usage. |
| **Checkpointing for free** | The file *is* a checkpoint; restart by reopening it. |

### Cons
| Con | Detail |
|-----|--------|
| **Disk I/O latency** | Each step incurs a synchronous write (mitigated by chunking/caching). |
| **Dependency** | Requires `h5py` (and HDF5 C library) or `zarr`. |
| **Not a pure NumPy array** | Code that expects `np.ndarray` must read slices explicitly. |
| **File management** | Must handle file open/close, corruption, and cleanup. |

---

## Option 4: Buffer-Then-Concatenate (Deferred Copy)

### Concept
Accumulate incoming time steps in **cheap Python lists** (`list.append` is O(1) amortized). Periodically (or at the end) **concatenate once** per key. This minimizes the number of large copies.

### Storage structure
```python
self.__buffer = {label: [] for label in state_sizes}
self.__storage = {}            # final arrays, or None until flushed
FLUSH_EVERY = 10_000           # tune to memory budget
```

### One-line buffer step
```python
[
    self.__buffer[label].append(values)
    for label, values in data.items()
]
```

### Periodic flush (batched copy)
```python
if len(next(iter(self.__buffer.values()))) >= FLUSH_EVERY:
    for label, buf in self.__buffer.items():
        if buf:
            new = np.stack(buf, axis=1)               # shape (N, FLUSH_EVERY)
            old = self.__storage.get(label, np.empty((N, 0)))
            self.__storage[label] = np.concatenate([old, new], axis=1)
            buf.clear()
```

### Pros
| Pro | Detail |
|-----|--------|
| **Simple conceptual model** | Python list for fast appends; NumPy only when needed. |
| **Minimal copies per step** | No copy during the buffer phase; only one copy per flush. |
| **Works with any downstream code** | `self.__storage` is a plain `dict[str, np.ndarray]`. |
| **No external dependencies** | Pure NumPy + Python. |

### Cons
| Con | Detail |
|-----|--------|
| **Still copies data eventually** | Each flush copies the entire accumulated buffer + existing array. |
| **Latency spikes** | Flush can cause a noticeable pause if arrays are huge. |
| **Memory doubling during flush** | Old array + new concatenated array coexist briefly. |
| **Not truly zero-copy** | If the requirement is *never* copy, this fails. |

---

## Summary Comparison

| Criterion | Pre-Allocate | Chunked List | On-Disk (h5py) | Buffer-Then-Concat |
|---|---|---|---|---|
| **Zero copy of existing data** | ✅ | ✅ | ✅ | ❌ (deferred) |
| **True single-line update** | ✅ | ❌ (needs small loop) | ❌ (needs small loop) | ✅ (buffer line) |
| **Handles unbounded growth** | ❌ (needs max estimate) | ✅ | ✅ | ✅ |
| **RAM only** | ✅ | ✅ | ❌ (disk-backed) | ✅ |
| **Complexity** | Low | Medium | Medium–High | Low |
| **External deps** | None | None | `h5py` / `zarr` | None |
| **Best for "trillions of steps"** | Only if max known | ✅ Good fit | ✅ Best fit | ❌ Copy cost grows |

---

## Recommendation for `Truth_Component`

Given the stated constraints (**trillions of time steps**, **no copying of existing data**, **single time step per call**):

1. **If the simulation can be bounded** (you can estimate an upper step count), **Option 1 (pre-allocate)** is the simplest and fastest — a true one-liner update with zero overhead.

2. **If the step count is unknown or genuinely unbounded**, **Option 2 (chunked list)** gives you unbounded growth with no copies and keeps everything in RAM. The update is a few lines but easily wrapped in a helper method to keep call sites clean.

3. **If data will eventually exceed RAM or you want persistence**, **Option 3 (h5py/zarr)** is the production-grade solution used in HPC and data acquisition systems.

For the `Truth_Component.store_data` method, wrapping **Option 2** in a small private helper gives the caller a clean, one-line interface:

```python
def store_data(self, data: dict[str, np.ndarray]) -> None:
    self._append_step(data)   # internally chunk-managed, no visible loop
```