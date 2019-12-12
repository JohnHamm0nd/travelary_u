from .data.models import Data
from django_seed import Seed
import csv


seeder = Seed.seeder()

 
f = open('a.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    print(line)
f.close() 

# seeder.add_entity(Player, 10, {
#     'score':    lambda x: random.randint(0,1000),
#     'nickname': lambda x: seeder.faker.email(),
# })
# seeder.execute()