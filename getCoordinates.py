from dadata import Dadata
token = "b62ae929ec2cd2fde502644f29599e1abbf9942f"
secret = "498c88999fd9cb0009421c51f55aa3e83ac01036"


def get_location(address):
    location = tuple()
    dadata = Dadata(token, secret)
    result = dadata.clean("address", address)
    location = (result['geo_lon'], result['geo_lat'])
<<<<<<< HEAD
    return location


def get_coordinates(address):
    dadata = Dadata(token, secret)
    result = dadata.clean('address', address)
    return result['geo_lon'], result['geo_lat']
=======
    return location
>>>>>>> 8583930 (Добавил простую регистрацию, потом переделаю, чтобы что-то было, добавить отметки на карте, чтобы круто смотрелось и повысим городскую инклюзивность, пока что всё, потом по хорошему если 2гис ответят перейти к ним))
