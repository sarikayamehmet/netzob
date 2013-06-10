#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Georges Bossert <georges.bossert (a) supelec.fr>                  |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+
from netzob.Common.Models.Vocabulary.Domain.Alt import Alt
from netzob.Common.Models.Vocabulary.Domain.Agg import Agg
from netzob.Common.Models.Types.Decimal import Decimal
from netzob.Common.Models.Types.ASCII import ASCII
from netzob.Common.Models.Types.AbstractType import AbstractType


class DomainFactory(object):
    """This factory allows to manipulate a domain as for example to normalize it.

    For instance, you can normalize domains provided by users

    >>> from netzob import *
    >>> domain = DomainFactory.normalizeDomain([Raw(), 10])
    >>> print domain.nodeType
    Alt
    >>> print domain.children[0].__class__.__name__
    Raw
    >>> print domain.children[1].__class__.__name__
    Decimal

    >>> domain = DomainFactory.normalizeDomain(Agg([Alt(["toto", 20]), ASCII("!")]))
    >>> print domain.nodeType
    Agg
    >>> print domain.children[0].nodeType
    Alt
    >>> print domain.children[0].children[1].__class__.__name__
    Decimal
    >>> print domain.children[1].__class__.__name__
    ASCII

    """

    @staticmethod
    def normalizeDomain(domain):
        # If domain starts with an Alternative (or a list)
        if isinstance(domain, (list, Alt)):
            return DomainFactory.__normalizeAlternateDomain(domain)
        # If domain starts with an Aggregate
        elif isinstance(domain, Agg):
            return DomainFactory.__normalizeAggregateDomain(domain)
        else:
            return DomainFactory.__normalizeLeafDomain(domain)

    @staticmethod
    def __normalizeLeafDomain(domain):
        if isinstance(domain, int):
            return Decimal(value=domain)
        elif isinstance(domain, str):
            return ASCII(value=domain)
        elif isinstance(domain, AbstractType):
            return domain

    @staticmethod
    def __normalizeAlternateDomain(domain):
        result = Alt()
        if isinstance(domain, list):
            for child in domain:
                result.children.append(DomainFactory.normalizeDomain(child))
        elif isinstance(domain, Alt):
            for child in domain.children:
                result.children.append(DomainFactory.normalizeDomain(child))
        else:
            raise TypeError("Impossible to normalize the provided domain as an alternate.")
        return result

    @staticmethod
    def __normalizeAggregateDomain(domain):
        result = Agg()
        if isinstance(domain, Agg):
            for child in domain.children:
                result.children.append(DomainFactory.normalizeDomain(child))
        else:
            raise TypeError("Impossible to normalize the provided domain as an aggregate.")
        return result