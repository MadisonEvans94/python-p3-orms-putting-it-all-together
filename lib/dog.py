import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None): 
        self.name = name
        self.breed = breed
        self.id = id
        
    def create_table(): 
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                breed TEXT NOT NULL
            )
        ''')
        CONN.commit()
        
    def drop_table(): 
        # Class Dog in dog.py contains method "drop_table()" that drops table "dogs" if it exists
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        CONN.commit()

    def save(self): 
        CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog
    
    @staticmethod
    def get_all():
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = Dog.new_from_db(row)
            dogs.append(dog)
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute('SELECT * FROM dogs WHERE id=?', (id,))
        result = CURSOR.fetchone()
        if result:
            return cls.new_from_db(result)
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        # Check if the dog already exists in the database
        CURSOR.execute('SELECT * FROM dogs WHERE name=? AND breed=?', (name, breed))
        row = CURSOR.fetchone()
        if row:
            # If the dog already exists, return a Dog instance corresponding to that record
            return cls.new_from_db(row)
        else:
            # If the dog doesn't exist, create a new record and return a Dog instance for that record
            dog = cls(name, breed)
            dog.save()
            return dog
        
    
    def update(self):
        if self.id is None:
            return
        
        CURSOR.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
        CONN.commit()