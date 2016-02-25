from hashlib import sha1

from numpy import all, array, uint8
import hashlib


def array_hash(array):
    """ Convert the given array into a hash value """
    # Time to execute 1000 runs < 11 seconds
    # b = array.view(uint8)
    # return hashlib.sha1(b).hexdigest()

    # Time to execute 1000 runs < 11 seconds
    # return int(sha1(array.view(uint8)).hexdigest(), 16)

    # Time to execute 1000 runs < 5 seconds
    # array.flags.writeable = False
    # hash_number = hash(array.data)
    # array.flags.writeable = True
    # return hash_number

    # Best time to execute 1000 runs 3.44 seconds
    return hash(str(array.data))


class Hashable(object):
    """
    Hashable wrapper for ndarray objects.

    Instances of ndarray are not hashable, meaning they cannot be added to
    sets, nor used as keys in dictionaries. This is by design - ndarray
    objects are mutable, and therefore cannot reliably implement the
    __hash__() method.

    The hashable class allows a way around this limitation. It implements
    the required methods for hashable objects in terms of an encapsulated
    ndarray object. This can be either a copied instance (which is safer)
    or the original object (which requires the user to be careful enough
    not to modify it).

    Source: http://machineawakening.blogspot.com.au/
    """
    def __init__(self, wrapped, tight=True):
        """
        Creates a new hashable object encapsulating an ndarray.

        :param wrapped: the wrapped ndarray
        :param tight: optional; if True a copy of the input ndaray is created
        """
        self.__tight = tight
        self.__wrapped = array(wrapped) if tight else wrapped
        self.__hash = int(sha1(wrapped.view(uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

    def unwrap(self):
        """
        Returns the encapsulated ndarray.

        If the wrapper is "tight", a copy of the encapsulated ndarray is
        returned. Otherwise, the encapsulated ndarray itself is returned.
        """
        if self.__tight:
            return array(self.__wrapped)

        return self.__wrapped