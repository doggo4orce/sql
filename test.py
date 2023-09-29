import dataclasses
import sqlite3

@dataclasses.dataclass
class column:
	name: str
	type: ...

	def __init__(self, name, typ):
		self.name = name
		if type(typ) == str:
			if typ.lower() == "text":
				self.type = str
			elif typ.lower() == "int":
				self.type = int
		elif typ in [int, str]:
			self.type = typ
		else:
			self.type = str # throw exception?

	@property
	def sqlite3_type(self):
		if self.type == int:
			return "int"
		elif self.type == str:
			return "text"
		else:
			return None # throw exception?

	def __str__(self):
		return f"('{self.name}', '{self.sqlite3_type}')"

class database:
	def __init__(self, db_file):
		self._connection = sqlite3.connect(db_file)
		self._cursor = self._connection.cursor()

	# wrapping cursor/connection functionality to database
	def execute(self, query):
		self._cursor.execute(query)
	def fetchone(self):
		return self._cursor.fetchone()
	def fetchall(self):
		return self._cursor.fetchall()

	def list_table_names(self):
		ret_val = list()

		self.execute("SELECT * FROM sqlite_master WHERE type='table'")

		for line in self.fetchall():
			ret_val.append(line[1])

		return ret_val

	def list_columns(self, table_name):
		ret_val = list()

		self.execute(f"PRAGMA table_info({table_name})")

		for idx, line in enumerate(self.fetchall()):
			ret_val.append((idx, column(line[1], line[2])))

		return ret_val

	def table_exists(self, table_name):
		return table_name in self.list_table_names()

	def create_table(self, table_name, *columns):
		if self.table_exists(table_name):
			return
		
		column_string = ""

		for column in columns:
			column_string += f"{column.name} {column.sqlite3_type},"

		#peel off last comma
		column_string = column_string[:-1]

		self.execute(f"CREATE TABLE {table_name}({column_string})")

	def insert(self, table_name, **values):
		pass
db = database(":memory:")

db.create_table("employees", column("first_name", str), column("last_name", str), column("age", int))

for column in db.list_columns("employees"):
	print(column)


db.execute("""INSERT INTO employees (first_name, last_name, age) VALUES ("kyle", "schlitt", 39);""")
db.execute("PRAGMA table_info(employees)")
print(db.fetchall())

db.execute("""SELECT * FROM employees""")
print(db.fetchall())

#db.insert("employees", first_name="kyle", last_name="schlitt", age=39)

#db.select("employees", name="kyle")
