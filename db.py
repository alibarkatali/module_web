import psycopg2, urlparse, re, os
import urlparse

# url de la base de donnees heroku
#DATABASE_URL="postgres://eoxdsmbgnnjprd:819342ac1961db6dceb37078f90e581b45743e34502382e75184184eae7b1948@ec2-23-21-220-152.compute-1.amazonaws.com:5432/decknecom629ch"

class Db:
  """Connexion a la base de donnees postgres de l'environnement Heroku."""

  def __init__(self):
    """Initiate a connection to the default postgres database."""

    # connexion a la base de donnees locale
    url = urlparse.urlparse("postgresql://imerir:imerir@localhost/imerir")

    #connexion base de donnees heroku
    #urlparse.uses_netloc.append("postgres")
    #url = urlparse.urlparse(os.environ["DATABASE_URL"])

    self.conn = psycopg2.connect(
       database=url.path[1:],
       user=url.username,
       password=url.password,
       host=url.hostname,
       port=url.port
    )
    self.cur = self.conn.cursor()

  def describeRow(self, row, columns, subkeys = None):
    dRow = dict()
    if subkeys == None:
      for (i,cName) in enumerate(columns):
        dRow[cName] = row[i]
    else:
      for (i,cName) in enumerate(columns):
        k = cName if cName not in subkeys else subkeys[cName]
        if k != "":
          dRow[k] = row[i]
    return dRow

  def rowcount(self):
    return self.cur.rowcount

  def lastrowid(self):
    return self.cur.lastrowid

  def fetchall(self, subkeys = None):
    rows  = self.cur.fetchall()
    if rows != None:
      columns = map(lambda d: d[0], self.cur.description)
      rows = [self.describeRow(row, columns, subkeys) for row in rows]
    else:
      rows = []
    return rows

  def fetchone(self, subkeys = None):
    row = self.cur.fetchone()
    if row != None:
      columns = map(lambda d: d[0], self.cur.description)
      row = self.describeRow(row, columns, subkeys)
    return row

  def execute(self, sql, sqlParams=None):
    if sqlParams == None:
      self.cur.execute(sql)
    else:
      sql = re.sub(r"@\(([^\)]+)\)", "%(\g<1>)s", sql)
      self.cur.execute(sql, sqlParams)
    self.conn.commit()
  def select(self, sql, sqlParams=None, subkeys=None):
    self.execute(sql, sqlParams)
    return self.fetchall(subkeys)

  def close(self):
    self.cur.close()
    self.conn.close()

  def executeFile(self, filename):
    f = file(filename, "r")
    sql = f.read()
    f.close()
    self.execute(sql)
