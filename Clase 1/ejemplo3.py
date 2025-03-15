año = int(input("Ingrese un año: "))
es_bisiesto = (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)
print(f"¿El año {año} es bisiesto? {es_bisiesto}")
#TODO averiguar operador igual e identico