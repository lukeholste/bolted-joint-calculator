
"""
Bolted joint class definition
Screw joint class definition
Dictionary definitions for:
    - Materials
    - Strength classes
    - Bolt sizes
"""

MATERIALS = {"steel": {"E": 200e9, "Sy": 250e6, "v": 0.3}, 
             "aluminium": {"E": 70e9, "Sy": 100e6, "v": 0.33},
               "copper": {"E": 100e9, "Sy": 70e6, "v": 0.35},
               "titanium": {"E": 110e9, "Sy": 100e6, "v": 0.34},
                "brass": {"E": 100e9, "Sy": 100e6, "v": 0.34},
}

STRENGTH_CLASSES = {}

BOLT_SIZES = {}

BOLT_SIZES_STR = {
    """Bolt Size: (shank diameter, cross section, effective cross section, threads per inch)"""
    "8-32": {"A_d": 0.164, "A": 0.164, "A_t": 0.164, "TPI": 32},

    }

def print_dict_keys(dictionary) -> None: 
    for key in dictionary.keys():
        print(key)

class Member:
    """
    Member class definition
    """
    _member_id = 0
    def __init__(self, material, thickness, hole_diameter=None, name):
        #Thickness must be a positive number
        if thickness <= 0:
            raise ValueError("Member thickness must be a positive number")
        if material not in MATERIALS.keys():
            raise ValueError("Invalid material")
        
        self.name = name
        self.material = material
        self.thickness = thickness
        self.hole_diameter = hole_diameter
        self.E = MATERIALS[material]["E"]
        self.Sy = MATERIALS[material]["Sy"]
        self.v = MATERIALS[material]["v"]
        self.id = Member._member_id; Member._member_id += 1

    def __str__(self):
        return f"Member: \n    Material: {self.material}\n    Thickness: {self.thickness}"
    
    def __repr__(self):
        return f"Member(material={self.material!r}, thickness={self.thickness!r}, hole_diameter={self.hole_diameter!r})"
    
    def __add__(self, other):
        """
        Increase thickness of member by a value
        """
        return self.thickness + other
    def __sub__(self, other):
        """
        Decrease thickness of member by a value
        """
        return self.thickness - other
    
    def __iadd__(self, other):
        """
        Increase thickness of member by a value
        """
        self.thickness += other
        return self
    
    def __isub__(self, other):
        """
        Decrease thickness of member by a value
        """
        self.thickness -= other
        return self
    

class Bolt:
    """
    Bolt class definition
    """
    def __init__(self, diameter, material, strength, length=None):
        if isinstance(diameter, float) or isinstance(diameter, int):
            self.diameter = diameter
        elif isinstance(diameter, str):
            self.diameter = BOLT_SIZES_STR[diameter]
            if not self.diameter: #No match found, strip thread and look for a match
                diameter = diameter.split("-")[-1]
                if diameter in dict.keys: self.diameter, self.A, self.A_t, = BOLT_SIZES_STR[diameter]
                else:
                    print("No corresponding bolt size found in catalog.\nSee valid options below: ")
                    print_dict_keys(BOLT_SIZES_STR)
        else:
            pass
        self.material = material.lower()
        self.strength = strength

    def __str__(self):
        return f"Bolt: \n    Diameter: {self.diameter}\n    Material: {self.material}\n    Strength: {self.strength}"
    
    def __repr__(self):
        return f"Bolt(diameter={self.diameter!r}, material={self.material!r}, strength={self.strength!r})"



class BoltedJoint:
    """
    Bolted joint class definition
    Members should be listed in the order of assembly (from top (right below bolt) to bottom)
    """
    def __init__(self, bolt, *members, load=None):
        self.members = list(members)
        self.bolt = bolt
        self.load = load if load is not None else {"axial": 0, "shear": 0, "moment": 0}
    
    def __str__(self):
        members_str = "\n    ".join(str(member) for member in self.members)
        return f"Bolted Joint: \n    Members: \n    {members_str}\n    Bolt: {self.bolt}"
    
    def __repr__(self):
        return f"BoltedJoint(members={self.members!r}, bolt={self.bolt!r})"
    
    def add_load(self, type="axial", value=0): 
        """
        Add load to the joint
        """
        if type not in self.load:
            raise ValueError("Invalid load type")
        else: self.load[type] = value

    def add_member(self, member):
        """
        Add member to the joint
        """
        if not isinstance(member, Member):
            raise TypeError("member must be an instance of the Member class")
        
        self.members.append(member)
    
    def remove_member(self, member):
        """
        Remove member from the joint
        """
        self.members.remove(member)

    def change_bolt(self, bolt):
        """
        Change bolt in the joint
        """
        if not isinstance(bolt, Bolt):
            raise TypeError("bolt must be an instance of the Bolt class")
        self.bolt = bolt
    
    def calculate_joint_stiffness(self):
        """
        Calculate the combined stiffness of the joint 
        """
        
        self.k = 0
        
        pass
    def FOS_tension(self):
        """
        Factor of Safety for tension
        """
        if self.load["axial"] == 0:
            raise ValueError("No axial load applied")
        
        if self.k is None:
            self.calculate_joint_stiffness(self)
            
        pass
    
    def FOS_shear(self, P):
        """
        Factor of Safety for shear
        """
        pass
    
    