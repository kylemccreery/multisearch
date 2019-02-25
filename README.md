# multisearch
Scrapes local game store websites and formats the data in a standard way.

Currently only supports 3 local game stores in Hawaii (Oahu).

Supported stores:
+ Durdle Zone
+ Da-Planet
+ Ideal808
  
Each of these stores uses Crystal Commerce and can be queried with a JSON encoded URL, but they each use a different organizational structure. Crystal Commerce websites are notoriously slow, so the solution was for me to query all three at once, and compare the output simultaneously to easily see all prices and conditions of their stock.
# hiflgs
