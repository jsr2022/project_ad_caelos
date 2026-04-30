#integrator_factory.py
# Factory for creating integrator instances based on enum types
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.integrators.integrator_meta_interface import Integrator_Meta_Interface
from adcaelos.integrators.rk4 import RK4


class IntegratorFactory:
    """
    Factory that maps enum values to concrete integrator instances.
    
    Creates integrator instances based on the Integrator_Enums value,
    allowing TRUTH components to use pluggable numerical integration
    methods without tight coupling to specific implementations.
    """
    
    _registry = {
        Integrator_Enums.RK4: RK4,
        # Future: Integrator_Enums.RK5: RK5,
        # Future: Integrator_Enums.Euler: Euler,
    }
    
    @classmethod
    def create(cls, integrator_enum: Integrator_Enums) -> Integrator_Meta_Interface:
        """
        Create and return an integrator instance based on the enum.
        
        Parameters
        ----------
        integrator_enum : Integrator_Enums
            The enum value identifying which integrator to create
            
        Returns
        -------
        Integrator_Meta_Interface
            A new instance of the requested integrator
            
        Raises
        ------
        ValueError
            If the integrator type is not registered in the factory
        """
        if integrator_enum not in cls._registry:
            raise ValueError(
                f"Unknown integrator type: {integrator_enum}. "
                f"Available types: {list(cls._registry.keys())}"
            )
        return cls._registry[integrator_enum]()
    
    @classmethod
    def register(cls, enum_value: Integrator_Enums, integrator_class):
        """
        Register a new integrator type with the factory.
        
        Parameters
        ----------
        enum_value : Integrator_Enums
            The enum value to associate with this integrator
        integrator_class : type
            The integrator class (must implement Integrator_Meta_Interface)
        """
        cls._registry[enum_value] = integrator_class