# quicklog/models.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Commit:
    """
    Rappresenta un ingolo commit Git con le informazioni essenziali
    """
    hash_short: str   #Es: "fe15d03"
    hash_full: str    #Es: "fe15d03..."
    author_name: str   #Es: "Mario Rossi"
    author_email: str  #Es: "Mario.Rossi@email.com"
    timestamp : int    # Timestaamp Unix (es 16788888)
    message : str      # il mex del commit

    @property
    def date_str(self) -> str:
        """
        Restituisce l adata formattata leggibile (Es: '2023-11-19 14:30').
        Utile per la visualizzione nella UI.
        """

        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')