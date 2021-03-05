user_input = "Hello. Id'like to book a flight from Paris to New-York, leaving on Saturday, August 13, 2016 and returning on Tuesday, August 16, 2016. I have a budget of $3700."
my_string = "$3700"

start_index = user_input.find(my_string)
end_index = start_index + len(my_string) - 1
print(f"Start index : {start_index}")
print((f"End index : {end_index}"))