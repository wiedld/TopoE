import model
import csv


def load_gen_stats(session):
	with open('seed_data/test.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			gen_obj = model.StatsGen()
			gen_obj.utility_id = row[0]
			gen_obj.utility_name = row[1]
			gen_obj.plant_name = row[3]
			gen_obj.state = row[4]
			gen_obj.county = row[5]
			gen_obj.status = row[8]
			gen_obj.nameplate_MW = float(row[9])
			gen_obj.summer_MW = float(row[10])
			gen_obj.winter_MW = float(row[11])
			gen_obj.start_mo = row[13]
			gen_obj.start_yr = row[14]
			gen_obj.fuel_1 = row[15]
			gen_obj.fuel_2 = row[16]
			gen_obj.fuel_3 = row[17]
			gen_obj.fuel_4 = row[18]
			gen_obj.fuel_5 = row[19]
			gen_obj.fuel_6 = row[20]
			gen_obj.multi_fuel = row[21]
			gen_obj.interconnected = row[22]
			gen_obj.synchronized = row[23]

			session.add(gen_obj)
	session.commit()


def load_gen_prod(session):
	pass



def main(session):
	load_gen_stats(session)
	load_gen_prod(session)


if __name__ == "__main__":
	s=model.connect()
	main(s)
