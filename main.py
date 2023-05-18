import psycopg2


# Establish connection
conn = psycopg2.connect(
   database="pokemon", user='postgres', password='pokemon', host='127.0.0.1', port='5432')

# Create cursor
cursor = conn.cursor()


# Create Table
create_table_query = """create table if not exists pokemon(
pokedex int,
poke_name character varying,
type1 character varying, 
type2 character varying,
total int,
hp int, 
attack int,
defense int,
sp_atk int,
sp_def int,
speed int,
generation int,
legendary character varying
)
"""

cursor.execute(create_table_query)
conn.commit()

# Import CSV data: Once the code runs, comment this out.
# TODO: Find ways to improve this in order to prevent duplicate data  import
# with open('Pokemon.csv', 'r') as f:
#    next(f)
#    cursor.copy_from(f, 'pokemon', sep=',')
#    conn.commit()


# Function to make cleaner code
def run_query(query):
   cursor.execute(query)
   header = header = [i[0] for i in cursor.description]
   print(header)
   for table in cursor:
      print(table)

# 1. What are the top 5 strongest non-legendary monsters?
# A. If we think it terms of hit points (hp) alone:
strongest_hp = """
select poke_name, hp, legendary
from public.pokemon
where legendary='False'
order by hp desc limit 5
"""
print("QUESTION 1: What are the top 5 strongest non-legendary monsters?")

print("There are two ways to think of this. \n"
      "If we define 'strongest' as having the highest hit points:")
run_query(strongest_hp)

# B. If we think it terms of total stats (hp, attack, defense, special attack, special defense):
strongest_total = """
select poke_name, total, legendary
from public.pokemon
where legendary='False'
order by total desc limit 5
"""

print("If we define 'strongest' as having the highest overall stats:")
run_query(strongest_total)
print("")


# 2. Which Pokemon type has the highest average HP?
hp_type_query = """
select type1, avg(hp)
from pokemon
group by type1
order by type1 desc limit 1
"""

print("QUESTION 2: Which Pokemon type has the highest average HP?")
run_query(hp_type_query)
print("It would be the Water type with an average of 72 HPs \n")

# 3. Which is the most common special attack?
special_attack_query = """
select sp_atk, count(sp_atk) as count_of_sp_atk
from pokemon p 
group by sp_atk
order by count(sp_atk) desc limit 1
"""

print("QUESTION 3: Which is the most common special attack?")
run_query(special_attack_query)
print("The most common special attack is 60, with a count of 51.")

conn.close()