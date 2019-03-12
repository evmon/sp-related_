from django.test.testcases import TransactionTestCase

from station.models import (Transport, Spare, SpareProxy,
    PassengerСar, Truck, PlateNumberAbs, MilitaryNumber, SEATS_MAX,
    HEIGHT_MAX, WIDTH_MAX, CivilNumber, )
from .factories import (SpareFactory, ColorFactory, TruckFactory,
    PassengerСarFactory, MilitaryNumberFactory, CivilNumberFactory, )


class InheritanceTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        color = ColorFactory()
        color_2 = ColorFactory(name="Rose", shade="Printer's Magenta")
        color_3 = ColorFactory(name="Blue", shade="Blue Magenta")
        color_4 = ColorFactory(name="Black", shade="Black Magenta")
        SpareFactory()
        SpareFactory(country="Argentina", name="Mary Wheels")
        SpareFactory(country="UK", name="Filter")
        SpareFactory(country="UK", name="Happy Wheels")
        SpareFactory(country="Brazil", name="Brazil Wheels")
        TruckFactory(
            title="Plane",
            color=color,
            lifting_gear=True,
            width = 12.3,
            height = 121.1,
        )
        TruckFactory(title="Plane Test 1", color=color_4)
        PassengerСarFactory(title="Audi C8", color=color_2)
        PassengerСarFactory(
            title="Audi Test 3",
            color=color_3,
            hatch = False,
        )

    def test_get_spares_from_manager(self):
        spares_from_uk = SpareProxy.objects.country_uk()
        self.assertEquals(len(spares_from_uk), 2)
        self.assertEquals(spares_from_uk[0].name, 'Filter')
        self.assertEquals(spares_from_uk[1].name, 'Happy Wheels')

    def test_comparing_spare_objects(self):
        spares_default = Spare.objects.all()
        ordered_spares = SpareProxy.objects.all()
        self.assertNotEqual(spares_default, ordered_spares)

    def test_check_developed_country(self):
        usa_country = SpareProxy.objects.get(id=1)
        self.assertEquals(usa_country.country, 'USA')
        uk_country = SpareProxy.objects.get(id=2)
        self.assertEquals(uk_country.country, 'Argentina')
        blazil_country = SpareProxy.objects.get(id=5)
        self.assertEquals(blazil_country.country, 'Brazil')
        self.assertTrue(usa_country.is_dev())
        self.assertTrue(uk_country.is_dev())
        self.assertFalse(blazil_country.is_dev())

    def test_check_func_spareproxy_doesnt_exist(self):
        usa_country = Spare.objects.get(id=1)
        self.assertEquals(usa_country.country, 'USA')
        with self.assertRaises(AttributeError):
            is_dev = usa_country.is_dev()

    def test_check_truck_reliability(self):
        truck = Truck.objects.get(id=1)
        self.assertFalse(truck.is_reliable())
        self.assertGreater(truck.height, HEIGHT_MAX)
        self.assertLessEqual(truck.width, WIDTH_MAX)
        truck_2 = Truck.objects.get(id=2)
        self.assertLessEqual(truck_2.height, HEIGHT_MAX)
        self.assertLessEqual(truck_2.width, WIDTH_MAX)
        self.assertTrue(truck_2.is_reliable())

    def test_check_travel_permission(self):
        ps_car = PassengerСar.objects.get(id=3)
        self.assertTrue(ps_car.hatch)
        self.assertLessEqual(ps_car.seats, SEATS_MAX)
        self.assertTrue(ps_car.travel_permission())
        ps_car_2 = PassengerСar.objects.get(id=4)
        self.assertFalse(ps_car_2.hatch)
        self.assertLessEqual(ps_car_2.seats, SEATS_MAX)
        self.assertFalse(ps_car_2.travel_permission())

    def test_check_inheritance(self):
        self.assertTrue(issubclass(SpareProxy, Spare))
        self.assertTrue(issubclass(PassengerСar, Transport))
        self.assertTrue(issubclass(Truck, Transport))
        self.assertTrue(issubclass(MilitaryNumber, PlateNumberAbs))
        self.assertTrue(issubclass(CivilNumber, PlateNumberAbs))

    def test_get_info_civil_number(self):
        CivilNumberFactory()
        civil_obj = CivilNumber.objects.get(id=1)
        self.assertEquals(civil_obj.serial, 'AA')
        self.assertEquals(civil_obj.get_plate_number(), 'AA6572')

    def test_get_info_millitary_number(self):
        MilitaryNumberFactory()
        military_obj = MilitaryNumber.objects.get(id=1)
        self.assertEquals(military_obj.serial, 'E1')
        self.assertEquals(military_obj.get_plate_number(), '9990 E1')
