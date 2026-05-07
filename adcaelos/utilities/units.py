#Class containing all unit conversions

class Units:
    ##-------------UNIT-CONVERSIONS-------------
    @staticmethod
    def in2cm() -> float:
        """Inch to Centimeter"""
        return 2.54
    
    @staticmethod
    def cm2in() -> float:
        """Centimeter to Inch"""
        return 1/Units.in2cm()

    @staticmethod
    def ft2m() -> float:
        """Feet to Meter"""
        return 0.3048
    
    @staticmethod
    def m2ft() -> float:
        """Meter to Feet"""
        return 1/Units.ft2m()
    
    @staticmethod
    def kg2lb() -> float:
        """Kilogram to Pound Mass"""
        return 1/Units.lb2kg()
    
    @staticmethod
    def lb2kg() -> float:
        """Pound Mass to Kilogram"""
        return 0.45359237 #exact U.S. Definition of a Pound (described in kg)
    
    @staticmethod
    def nmi2km() -> float:
        """Nautical Mile to Kilometer"""
        return 1.852
    
    @staticmethod
    def mi2km() -> float:
        """Mile to Kilometer"""
        return 5280*Units.ft2m()/1000
    
    @staticmethod
    def km2mi() -> float:
        """Kilometer to Mile"""
        return 1/Units.mi2km()
    
    @staticmethod
    def km2nmi() -> float:
        """Kilometer to Nautical Mile"""
        return 1/Units.nmi2km()
    
    @staticmethod
    def nmi2mi() -> float:
        """Nautical Mile to Mile"""
        return Units.nmi2km()/Units.mi2km()