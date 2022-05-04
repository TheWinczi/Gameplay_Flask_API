from enum import Enum, unique


@unique
class Roles(Enum):
    """ Enumerate object contains all existing roles
    and useful functions for roles management.
    """
    UNDEFINED = 0
    ADMIN = 1
    GUEST = 2

    __roles_dict = {
        UNDEFINED: 'undefined',
        ADMIN: 'admin',
        GUEST: 'guest'
    }

    @property
    def to_int(self):
        return int(self.value)

    @classmethod
    def to_str(cls, role: int) -> str:
        """ Map int role value to string
        representation of that role.

        Parameters
        ----------
        role : int
            Role to map.

        Returns
        -------
        role : str
            Mapped provided role.
        """
        if not isinstance(role, int):
            return cls.__roles_dict.value.get(Roles.UNDEFINED, 'undefined').upper()

        return cls.__roles_dict.value.get(role, 'undefined').upper()

    @classmethod
    def from_int(cls, role: int):
        """ Map int role value to Roles class
        enum value of that role.

        Parameters
        ----------
        role : int
            Role to map.

        Returns
        -------
        role : Roles
            Mapped provided role.
        """
        if not isinstance(role, int):
            return Roles.UNDEFINED

        for key, value in cls.__roles_dict.value.items():
            if key == role:
                return key
        return Roles.UNDEFINED

    @classmethod
    def from_str(cls, role: str) -> int:
        """ Map str role value to Roles class
        enum value of that role.

        Parameters
        ----------
        role : str
            Role to map.

        Returns
        -------
        role : int
            Mapped provided role.
        """
        if not isinstance(role, str):
            return Roles.UNDEFINEDS

        role = role.lower()
        for key, value in cls.__roles_dict.value.items():
            if value == role:
                return key
        return cls.UNDEFINED
