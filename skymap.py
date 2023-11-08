from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord, AltAz
from astropy import units as u
from astropy.time import Time
from skyfield.api import load, Topos
from datetime import datetime
from astropy.coordinates import EarthLocation

class skymap():
    def __init__(self, location:list) -> None:
        self.location = location if len(location) == 3 else location + [0]

    # Función para obtener coordenadas topográficas con astroquery
    def __get_astroquery(self, nombre_objeto, location:list, time:Time):
        customSimbad = Simbad()
        customSimbad.TIMEOUT = 120
        customSimbad.TIMEOUT = 300

        # Consulta el catálogo de Simbad
        result_table = customSimbad.query_object(nombre_objeto)

        if result_table is not None:
            # Obtiene las coordenadas equatoriales J2000
            ra = result_table['RA'][0]
            dec = result_table['DEC'][0]

            coordenadas = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))

            # Define una ubicación en la Tierra (puedes ajustar esto a tu ubicación específica)
            ubicacion_obs = EarthLocation(lat=location[0]*u.deg, lon=location[1]*u.deg, height=location[2]*u.m)

            # Convierte las coordenadas a coordenadas topográficas (altitud y azimut)
            coordenadas_topograficas = coordenadas.transform_to(AltAz(obstime=time, location=ubicacion_obs))
            return coordenadas_topograficas.alt.deg, coordenadas_topograficas.az.deg
        
        else:
            return None, None

    # Función para obtener coordenadas topográficas con Skyfield
    def __get_skyfield(self, nombre_objeto, location:list, tiempo_actual:datetime):
        eph = load('de421.bsp')

        ubicacion = Topos(latitude_degrees=location[0], longitude_degrees=location[1])

        try:
            ts = load.timescale()
            try:
                objeto_celeste = eph[nombre_objeto]
            except:
                objeto_celeste = eph[nombre_objeto + " barycenter"]

            # Calculamos las coordenadas topográficas en el tiempo actual
            astrometric = (eph['earth'] + ubicacion).at(ts.utc(tiempo_actual.year, tiempo_actual.month, tiempo_actual.day))
            topo = astrometric.observe(objeto_celeste)
            altitud, azimut, distancia = topo.apparent().altaz()

            return altitud.degrees, azimut.degrees
        except KeyError:
            return None, None

    # Función para obtener coordenadas topográficas con respaldo
    def get_coords(self, nombre_objeto, time_o:Time=None):
        time = time_o if time_o is not None else Time.now()

        altitud, azimut = self.get_astroquery(nombre_objeto, self.location, time)

        if altitud is not None and azimut is not None:
            return altitud, azimut
        else:
            return self.get_skyfield(nombre_objeto, self.location, time.to_datetime())



if __name__ == "__main__":
    skymapper = skymap([38.275451, -0.614771])
    map = skymapper.get_coords("Mars")
    print(map)


jgfufu