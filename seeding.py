import model
import csv
from datetime import datetime



def load_gen_prod_2014(session):
	with open('seed_data/gen_production_2014.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			print ("row:", row)		# troubleshooting.  If issue, see where.
			gen_obj = model.ProdGen()

			gen_obj.plant_id = row[0]
			gen_obj.chp = row[1]
			gen_obj.plant_name = row[3]	
			gen_obj.operator_name = row[4]
			gen_obj.operator_id = row[5]
			gen_obj.state = row[6]
			gen_obj.census_region = row[7]
			gen_obj.nerc_region = row[8]
			gen_obj.naics = row[10]
			gen_obj.sector_eia_id = row[11]
			gen_obj.sector_name = row[12]
			gen_obj.prime_mover = row[13]
			gen_obj.fuel_type = row[14]
			gen_obj.aer_fuel_type = row[15]

			#  some of the data is written as x,xxx.   Or is blank.
			#  since this occurs for 24 rows...make the action repeatitive.
			for index in range(67,91):
				print ("value:", row[index])
				if (row[index] == ".") or (row[index] is None) or (row[index] is ""):
					row[index] = float(0)
				else:
					new_value = float(  (row[index]).replace(",", "") )
					row[index] = new_value

			gen_obj.jan_fuel_consumed = row[67]
			gen_obj.feb_fuel_consumed = row[68]
			gen_obj.mar_fuel_consumed = row[69]
			gen_obj.apr_fuel_consumed = row[70]
			gen_obj.may_fuel_consumed = row[71]
			gen_obj.jun_fuel_consumed = row[72]
			gen_obj.jul_fuel_consumed = row[73]
			gen_obj.aug_fuel_consumed = row[74]
			gen_obj.sep_fuel_consumed = row[75]
			gen_obj.oct_fuel_consumed = row[76]
			gen_obj.nov_fuel_consumed = row[77]
			gen_obj.dec_fuel_consumed = row[78]

			gen_obj.jan_mwh_gen = row[79]
			gen_obj.feb_mwh_gen = row[80]
			gen_obj.mar_mwh_gen = row[81]
			gen_obj.apr_mwh_gen = row[82]
			gen_obj.may_mwh_gen = row[83]
			gen_obj.jun_mwh_gen = row[84]
			gen_obj.jul_mwh_gen = row[85]
			gen_obj.aug_mwh_gen = row[86]
			gen_obj.sep_mwh_gen = row[87]
			gen_obj.oct_mwh_gen = row[88]
			gen_obj.nov_mwh_gen = row[89]
			gen_obj.dec_mwh_gen = row[90]

			session.add(gen_obj)

		session.commit()




def load_gen_stats(session):
	# with open('seed_data/test.csv', 'rb') as csvfile:
	with open('seed_data/gen_stats.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, dialect='excel')
		for row in reader:
			print ("row:", row)		# troubleshooting.  If issue, see where.
			gen_obj = model.StatsGen()

			gen_obj.utility_id = row[0]
			gen_obj.utility_name = row[1]
			gen_obj.plant_name = row[3]
			gen_obj.state = row[4]
			gen_obj.county = row[5]
			gen_obj.status = row[8]

			#  some of the data is written as x,xxx.   Or is blank.
			if (row[9] is not None) and (row[9] is not ""):
				gen_obj.nameplate_MW = float(  (row[9]).replace(",", "") )
			if (row[10] is not None) and (row[10] is not ""):
				gen_obj.summer_MW = float( (row[10]).replace(",","") )
			if (row[11] is not None) and (row[11] is not ""):
				gen_obj.winter_MW = float( (row[11]).replace(",","") )

			#  a few of the months are incorrect.  E.g. "88" as a month.
			if int(row[13])>0 and int(row[13])<13:
				starting_mo_yr = str(row[13]) + "-" + str(row[14])
				gen_obj.start_mo = datetime.strptime(starting_mo_yr, "%m-%Y")
			else:
				gen_obj.start_mo = datetime.strptime(row[14], "%Y")

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




def main(session):
	# load_gen_stats(session)
	load_gen_prod_2014(session)


if __name__ == "__main__":
	s=model.connect()
	main(s)
