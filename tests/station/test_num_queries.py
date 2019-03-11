from django.db.models import Prefetch
from django.test.testcases import TransactionTestCase

from station.models import Transport, Client, Wheel
from .factories import (SpareFactory, TransportFactory, ClientFactory,
    TypeFactory, ColorFactory, WheelFactory, )

class NumQueriesTestCase(TransactionTestCase):
    reset_sequences = True # sequences reset before the test run
 
    def setUp(self):
        type_1 = TypeFactory()
        type_2 = TypeFactory(name="Notched")
        color = ColorFactory()
        color_2 = ColorFactory(name="Rose", shade="Printer's Magenta")
        spare = SpareFactory()
        spare_2 = SpareFactory(country="USA", name="Mary Wheels")
        spare_3 = SpareFactory(country="UK", name="Filter")
        spare_4 = SpareFactory(country="UK", name="Happy Wheels")
        tr = TransportFactory(title="Plane", color=color)
        tr_2 = TransportFactory(title="Audi C8", color=color_2)
        spare.types.add(type_1, type_2)
        tr.spares.add(spare, spare_2)
        tr_2.spares.add(spare_2, spare_3)
        wheel = WheelFactory()
        wheel.transports.add(tr, tr_2)
        
        ClientFactory(transport=tr)
        ClientFactory(
            transport=tr_2,
            name="Semen Uvik",
            phone="+380990000909",
            address="Ukraine",
        )
        self.names = []

    def test_transports_per_spare(self):
        def _get_transports_per_spare():
            client = Client.objects.first() # hits the database
            transport = client.transport # hits the database
            for spare in transport.spares.all(): # hits the database
                # hits the database twice
                for _type in spare.types.all():
                    self.names.append(_type.name)

        with self.assertNumQueries(5):
            _get_transports_per_spare()
        assert self.names == ['Circular', 'Notched']

    def test_get_transport_info(self):
        def _get_transports_info():
            clients = Client.objects.all()
            # hits the database
            client = clients.order_by('transport__title').last()
            # client.transport hits the database
            # transport.color hits the database
            transport = client.transport
            color = transport.color
            name = color.name
            shade = color.shade
            assert transport.title == 'Plane'
            assert client.name == 'Evheniya Monastyrna'
            assert [name, shade] == ["Red", "Burgundy"]
            
            for spare in transport.spares.all():
                for _type in spare.types.all():
                    self.names.append(_type.name)

        with self.assertNumQueries(6):
            _get_transports_info()

        assert self.names == ['Circular', 'Notched']

    def test_transports_wheels(self):
        def _get_transports_wheels():
            wheel = Wheel.objects.first() # hits the database
            for transport in wheel.transports.all(): # hits the database
                self.names.append(transport.color.name)

        with self.assertNumQueries(4):
            _get_transports_wheels()

        assert self.names == ['Red', 'Rose']

    # using select_related and prefetch_related
    def test_related_transports_per_spare(self):
        def _get_transports_per_spare():
            # Hits the database 3 times
            client = Client.objects.select_related(
                'transport').prefetch_related(
                    'transport__spares__types').first()
            transport = client.transport
            spares = transport.spares.all()
            for spare in spares:
                for _type in spare.types.all():
                    self.names.append(_type.name)

        with self.assertNumQueries(3):
            _get_transports_per_spare()
        assert self.names == ['Circular', 'Notched']

    def test_related_transports_info(self):
        def _get_transports_info():
            # Hits the database 3 times
            client = Client.objects.all().select_related(
                'transport__color').prefetch_related(
                    'transport__spares__types')\
                .order_by('transport__title').last()

            transport = client.transport
            color = transport.color
            name = color.name
            shade = color.shade
            assert transport.title == 'Plane'
            assert client.name == 'Evheniya Monastyrna'
            assert [name, shade] == ["Red", "Burgundy"]

            for spare in transport.spares.all():
                for _type in spare.types.all():
                    self.names.append(_type.name)

        with self.assertNumQueries(3):
            _get_transports_info()

        assert self.names == ['Circular', 'Notched']

    def test_related_transports_wheels(self):
        def _get_transports_wheels():
            # Hits the database twice
            wheel = Wheel.objects.prefetch_related(
                Prefetch(
                    'transports',
                    queryset=Transport.objects.select_related('color')
                )).first()
            transports = wheel.transports.all()
            for transport in transports:
                self.names.append(transport.color.name)

        with self.assertNumQueries(2):
            _get_transports_wheels()
        assert self.names == ['Red', 'Rose']
