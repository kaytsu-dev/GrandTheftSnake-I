"""Grand Theft Snake — original top-down retro open-world prototype."""
from __future__ import annotations

import json
import math
import random
import sys
from array import array
from functools import lru_cache
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent
SAVE_FILE = ROOT / "settings.json"
W, H = 480, 270
SCALE = 3
FPS = 60

PALETTE = {
    "ink": (8, 12, 20), "night": (13, 20, 30), "panel": (17, 27, 39),
    "white": (236, 239, 224), "muted": (144, 160, 167), "mint": (98, 233, 180),
    "amber": (255, 190, 87), "red": (238, 91, 89), "blue": (75, 157, 217),
}

CHARACTERS = [
    {"name": "NICO", "tag": "TAG_MECHANIC", "coat": (58, 159, 180), "skin": (226, 179, 135)},
    {"name": "MARA", "tag": "TAG_COURIER", "coat": (207, 91, 96), "skin": (194, 143, 111)},
    {"name": "TEO", "tag": "TAG_NAVIGATOR", "coat": (174, 143, 74), "skin": (194, 151, 115)},
    {"name": "LIA", "tag": "TAG_RUNNER", "coat": (123, 108, 177), "skin": (222, 183, 146)},
]

VEHICLE_NAME_KEYS = {
    "BERLINA": "CAR_SEDAN", "COUPÉ": "CAR_COUPE", "TAXI": "CAR_TAXI",
    "SPORTIVA": "CAR_SPORT", "COMPACT": "CAR_COMPACT",
}

TEXT = {
    "it": {
        "NEW_GAME": "NUOVA PARTITA", "SETTINGS": "IMPOSTAZIONI", "EXIT": "ESCI",
        "MUSIC": "MUSICA", "SFX": "EFFETTI", "FULLSCREEN": "SCHERMO INTERO", "LANGUAGE": "LINGUA",
        "ITALIAN": "ITALIANO", "ENGLISH": "INGLESE", "FRENCH": "FRANCESE", "SPANISH": "SPAGNOLO", "ON": "SI", "OFF": "NO",
        "CHANGE_SETTING": "SINISTRA / DESTRA PER CAMBIARE", "BACK": "ESC  INDIETRO",
        "TAG_MECHANIC": "IL MECCANICO", "TAG_COURIER": "LA CORRIERA", "TAG_NAVIGATOR": "IL NAVIGATORE", "TAG_RUNNER": "LA STAFFETTA",
        "CHOOSE_CHARACTER": "SCEGLI IL TUO PERSONAGGIO", "CHARACTER_CONTROLS": "FRECCE / A-D PER CAMBIARE   •   INVIO PER CONTINUARE",
        "LOADING": "CARICAMENTO DI LIBERTY BAY", "PREPARING_CITY": "PREPARAZIONE DELLA CITTA'...",
        "FIND_PHONE": "TROVA UN TELEFONO E ACCETTA L'INCARICO", "PRESS_KEY": "PREMI UN TASTO",
        "PUBLISHER": "PUBLISHER", "CREATED_BY": "SVILUPPO E CREAZIONE", "PRESENTS": "SN COLORS  /  PRESENTA",
        "SLOGAN": "UNA CITTA'. UNA FUGA. LE TUE REGOLE.", "PROTOTYPE": "PROTOTIPO PYTHON  /  2026",
        "CITY": "LIBERTY BAY", "WANTED": "RIC:", "MISSION_DONE": "FATTO", "BAGS": "BUSTE {count}/4",
        "CAR_SEDAN": "BERLINA", "CAR_COUPE": "COUPE", "CAR_TAXI": "TAXI", "CAR_SPORT": "SPORTIVA", "CAR_COMPACT": "UTILITARIA",
        "GARAGE": "RIMESSA", "PHONE": "F: TELEFONO", "SCORE": "PTS {score}  x{multiplier}",
        "WALKING": "A PIEDI", "NO_CAR": "NESSUNA AUTO VICINA", "DRIVING": "AL VOLANTE",
        "CAR_STOLEN": "FURTO D'AUTO - RICERCATO!", "EMPTY_GUN": "PISTOLA SCARICA", "NO_PHONE": "NESSUN TELEFONO VICINO",
        "JOB1_START": "INCARICO ACCETTATO: RECUPERA 4 BUSTE", "JOB2_START": "NUOVO INCARICO: PORTA UN'AUTO RUBATA ALLA RIMESSA",
        "NO_MORE_JOBS": "INCARICHI DISPONIBILI: TORNA PIU' TARDI", "JOB1_ACTIVE": "INCARICO: RECUPERA LE QUATTRO BUSTE",
        "JOB2_ACTIVE": "INCARICO: AUTO RUBATA ALLA RIMESSA", "BUSTED": "ARRESTATO - MOLTIPLICATORE DIMEZZATO",
        "HEAT_COOLING": "ALLERTA IN CALO", "ASSAULT": "AGGRESSIONE - RICERCATO!",
        "POLICE_ATTACK": "ATTACCO ALLA POLIZIA!", "HIT_AND_RUN": "INVESTIMENTO - RICERCATO!",
        "BAG_REWARD": "BUSTA RECUPERATA +${amount}", "JOB_COMPLETE": "INCARICO COMPLETATO!",
        "CAR_DELIVERED": "AUTO CONSEGNATA - INCARICO COMPLETATO", "STOLEN_CAR_REQUIRED": "LA RIMESSA VUOLE UN'AUTO RUBATA",
        "BRIBE_USED": "MAZZETTA: RICERCATO AZZERATO", "AMMO_PICKUP": "PISTOLA: 6 COLPI", "CASH_PICKUP": "CASSA: +${amount}",
        "DISTRICT_ANNOUNCE": "DISTRETTO: {name}", "DISTRICT_CENTER": "VECCHIO CENTRO", "DISTRICT_UPTOWN": "UPTOWN",
        "DISTRICT_PORT": "IL PORTO", "DISTRICT_BAY": "BAIA SUD", "MISSION_PHONE": "F  RISPONDI", "STEAL_CAR": "E  RUBA AUTO",
        "EXIT_CAR": "E  SCENDI  /  {name}", "ENTER_CAR": "E  RUBA AUTO", "CONTROLS": "WASD / FRECCE",
        "PISTOL_AMMO": "PISTOLA {ammo}  SPACE", "RADIO_HINT": "R  RADIO", "RADIO_CHANGE": "RADIO: STAZIONE {station}", "RADIO_ON_FOOT": "LA RADIO FUNZIONA SOLO IN AUTO",
        "PAUSED": "PAUSA", "RESUME": "ESC RIPRENDI", "MAIN_MENU": "INVIO MENU PRINCIPALE",
    },
    "en": {
        "NEW_GAME": "NEW GAME", "SETTINGS": "SETTINGS", "EXIT": "QUIT",
        "MUSIC": "MUSIC", "SFX": "SOUND FX", "FULLSCREEN": "FULL SCREEN", "LANGUAGE": "LANGUAGE",
        "ITALIAN": "ITALIAN", "ENGLISH": "ENGLISH", "FRENCH": "FRENCH", "SPANISH": "SPANISH", "ON": "ON", "OFF": "OFF",
        "CHANGE_SETTING": "LEFT / RIGHT TO CHANGE", "BACK": "ESC  BACK",
        "TAG_MECHANIC": "THE MECHANIC", "TAG_COURIER": "THE COURIER", "TAG_NAVIGATOR": "THE NAVIGATOR", "TAG_RUNNER": "THE RUNNER",
        "CHOOSE_CHARACTER": "CHOOSE YOUR CHARACTER", "CHARACTER_CONTROLS": "ARROWS / A-D TO CHANGE   •   ENTER TO CONTINUE",
        "LOADING": "LOADING LIBERTY BAY", "PREPARING_CITY": "PREPARING THE CITY...",
        "FIND_PHONE": "FIND A PHONE AND TAKE THE JOB", "PRESS_KEY": "PRESS ANY KEY",
        "PUBLISHER": "PUBLISHER", "CREATED_BY": "DEVELOPED BY", "PRESENTS": "SN COLORS  /  PRESENTS",
        "SLOGAN": "ONE CITY. ONE GETAWAY. YOUR RULES.", "PROTOTYPE": "PYTHON PROTOTYPE  /  2026",
        "CITY": "LIBERTY BAY", "WANTED": "HEAT:", "MISSION_DONE": "DONE", "BAGS": "BAGS {count}/4",
        "CAR_SEDAN": "SEDAN", "CAR_COUPE": "COUPE", "CAR_TAXI": "TAXI", "CAR_SPORT": "SPORTS", "CAR_COMPACT": "COMPACT",
        "GARAGE": "GARAGE", "PHONE": "F: PHONE", "SCORE": "SCORE {score}  x{multiplier}",
        "WALKING": "ON FOOT", "NO_CAR": "NO CAR NEARBY", "DRIVING": "DRIVING",
        "CAR_STOLEN": "CARJACKING - WANTED!", "EMPTY_GUN": "OUT OF AMMO", "NO_PHONE": "NO PHONE NEARBY",
        "JOB1_START": "JOB ACCEPTED: COLLECT 4 ENVELOPES", "JOB2_START": "NEW JOB: DELIVER A STOLEN CAR TO THE GARAGE",
        "NO_MORE_JOBS": "NO MORE JOBS RIGHT NOW", "JOB1_ACTIVE": "JOB: COLLECT THE FOUR ENVELOPES",
        "JOB2_ACTIVE": "JOB: DELIVER A STOLEN CAR", "BUSTED": "BUSTED - MULTIPLIER HALVED",
        "HEAT_COOLING": "HEAT IS COOLING DOWN", "ASSAULT": "ASSAULT - WANTED!",
        "POLICE_ATTACK": "POLICE ASSAULT!", "HIT_AND_RUN": "HIT AND RUN - WANTED!",
        "BAG_REWARD": "ENVELOPE COLLECTED +${amount}", "JOB_COMPLETE": "JOB COMPLETE!",
        "CAR_DELIVERED": "CAR DELIVERED - JOB COMPLETE", "STOLEN_CAR_REQUIRED": "THE GARAGE WANTS A STOLEN CAR",
        "BRIBE_USED": "BRIBE: WANTED LEVEL CLEARED", "AMMO_PICKUP": "PISTOL: 6 ROUNDS", "CASH_PICKUP": "CRATE: +${amount}",
        "DISTRICT_ANNOUNCE": "DISTRICT: {name}", "DISTRICT_CENTER": "OLD TOWN", "DISTRICT_UPTOWN": "UPTOWN",
        "DISTRICT_PORT": "THE DOCKS", "DISTRICT_BAY": "SOUTH BAY", "MISSION_PHONE": "F  ANSWER", "STEAL_CAR": "E  STEAL CAR",
        "EXIT_CAR": "E  EXIT  /  {name}", "ENTER_CAR": "E  STEAL CAR", "CONTROLS": "WASD / ARROWS",
        "PISTOL_AMMO": "PISTOL {ammo}  SPACE", "RADIO_HINT": "R  RADIO", "RADIO_CHANGE": "RADIO: STATION {station}", "RADIO_ON_FOOT": "RADIO WORKS IN A CAR",
        "PAUSED": "PAUSED", "RESUME": "ESC TO RESUME", "MAIN_MENU": "ENTER FOR MAIN MENU",
    },
    "fr": {
        "NEW_GAME": "NOUVELLE PARTIE", "SETTINGS": "OPTIONS", "EXIT": "QUITTER",
        "MUSIC": "MUSIQUE", "SFX": "EFFETS SONORES", "FULLSCREEN": "PLEIN ECRAN", "LANGUAGE": "LANGUE",
        "ITALIAN": "ITALIEN", "ENGLISH": "ANGLAIS", "FRENCH": "FRANCAIS", "SPANISH": "ESPAGNOL", "ON": "OUI", "OFF": "NON",
        "CHANGE_SETTING": "GAUCHE / DROITE POUR MODIFIER", "BACK": "ECHAP  RETOUR",
        "TAG_MECHANIC": "LE MECANO", "TAG_COURIER": "LA COURRIERE", "TAG_NAVIGATOR": "LE NAVIGATEUR", "TAG_RUNNER": "LA MESSAGERE",
        "CHOOSE_CHARACTER": "CHOISIS TON PERSONNAGE", "CHARACTER_CONTROLS": "FLECHES / A-D POUR CHANGER   •   ENTREE POUR CONTINUER",
        "LOADING": "CHARGEMENT DE LIBERTY BAY", "PREPARING_CITY": "PREPARATION DE LA VILLE...",
        "FIND_PHONE": "TROUVE UN TELEPHONE ET ACCEPTE UN CONTRAT", "PRESS_KEY": "APPUYER SUR UNE TOUCHE",
        "PUBLISHER": "EDITEUR", "CREATED_BY": "DEVELOPPE PAR", "PRESENTS": "SN COLORS  /  PRESENTE",
        "SLOGAN": "UNE VILLE. UNE FUITE. TES REGLES.", "PROTOTYPE": "PROTOTYPE PYTHON  /  2026",
        "CITY": "LIBERTY BAY", "WANTED": "ALERTE:", "MISSION_DONE": "TERMINE", "BAGS": "LETTRES {count}/4",
        "CAR_SEDAN": "BERLINE", "CAR_COUPE": "COUPE", "CAR_TAXI": "TAXI", "CAR_SPORT": "SPORTIVE", "CAR_COMPACT": "CITADINE",
        "GARAGE": "GARAGE", "PHONE": "F: TELEPHONE", "SCORE": "SCORE {score}  x{multiplier}",
        "WALKING": "A PIED", "NO_CAR": "AUCUNE VOITURE PROCHE", "DRIVING": "AU VOLANT",
        "CAR_STOLEN": "VOL DE VOITURE - RECHERCHE!", "EMPTY_GUN": "PLUS DE MUNITIONS", "NO_PHONE": "AUCUN TELEPHONE PROCHE",
        "JOB1_START": "CONTRAT ACCEPTE: RECUPERE 4 LETTRES", "JOB2_START": "NOUVEAU CONTRAT: LIVRE UNE VOITURE VOLEE AU GARAGE",
        "NO_MORE_JOBS": "AUCUN AUTRE CONTRAT POUR LE MOMENT", "JOB1_ACTIVE": "CONTRAT: RECUPERE LES QUATRE LETTRES",
        "JOB2_ACTIVE": "CONTRAT: LIVRE UNE VOITURE VOLEE", "BUSTED": "ARRETE - MULTIPLICATEUR DIVISE PAR DEUX",
        "HEAT_COOLING": "LA PRESSION RETOMBE", "ASSAULT": "AGRESSION - RECHERCHE!",
        "POLICE_ATTACK": "ATTAQUE DE LA POLICE!", "HIT_AND_RUN": "DELI DE FUITE - RECHERCHE!",
        "BAG_REWARD": "LETTRE RECUPEREE +${amount}", "JOB_COMPLETE": "CONTRAT TERMINE!",
        "CAR_DELIVERED": "VOITURE LIVREE - CONTRAT TERMINE", "STOLEN_CAR_REQUIRED": "LE GARAGE VEUT UNE VOITURE VOLEE",
        "BRIBE_USED": "POT-DE-VIN: RECHERCHE ANNULEE", "AMMO_PICKUP": "PISTOLET: 6 BALLES", "CASH_PICKUP": "CAISSE: +${amount}",
        "DISTRICT_ANNOUNCE": "QUARTIER: {name}", "DISTRICT_CENTER": "VIEILLE VILLE", "DISTRICT_UPTOWN": "HAUTE VILLE",
        "DISTRICT_PORT": "LES DOCKS", "DISTRICT_BAY": "BAIE SUD", "MISSION_PHONE": "F  REPONDRE", "STEAL_CAR": "E  VOLER LA VOITURE",
        "EXIT_CAR": "E  SORTIR  /  {name}", "ENTER_CAR": "E  VOLER LA VOITURE", "CONTROLS": "WASD / FLECHES",
        "PISTOL_AMMO": "PISTOLET {ammo}  ESPACE", "RADIO_HINT": "R  RADIO", "RADIO_CHANGE": "RADIO: STATION {station}", "RADIO_ON_FOOT": "LA RADIO FONCTIONNE EN VOITURE",
        "PAUSED": "PAUSE", "RESUME": "ECHAP POUR REPRENDRE", "MAIN_MENU": "ENTREE POUR LE MENU",
    },
    "es": {
        "NEW_GAME": "NUEVA PARTIDA", "SETTINGS": "AJUSTES", "EXIT": "SALIR",
        "MUSIC": "MUSICA", "SFX": "EFECTOS", "FULLSCREEN": "PANTALLA COMPLETA", "LANGUAGE": "IDIOMA",
        "ITALIAN": "ITALIANO", "ENGLISH": "INGLES", "FRENCH": "FRANCES", "SPANISH": "ESPANOL", "ON": "SI", "OFF": "NO",
        "CHANGE_SETTING": "IZQUIERDA / DERECHA PARA CAMBIAR", "BACK": "ESC  VOLVER",
        "TAG_MECHANIC": "EL MECANICO", "TAG_COURIER": "LA MENSAJERA", "TAG_NAVIGATOR": "EL NAVEGANTE", "TAG_RUNNER": "LA CORREDORA",
        "CHOOSE_CHARACTER": "ELIGE TU PERSONAJE", "CHARACTER_CONTROLS": "FLECHAS / A-D PARA CAMBIAR   •   ENTER PARA CONTINUAR",
        "LOADING": "CARGANDO LIBERTY BAY", "PREPARING_CITY": "PREPARANDO LA CIUDAD...",
        "FIND_PHONE": "BUSCA UN TELEFONO Y ACEPTA EL TRABAJO", "PRESS_KEY": "PULSA UNA TECLA",
        "PUBLISHER": "EDITOR", "CREATED_BY": "DESARROLLADO POR", "PRESENTS": "SN COLORS  /  PRESENTA",
        "SLOGAN": "UNA CIUDAD. UNA HUIDA. TUS REGLAS.", "PROTOTYPE": "PROTOTIPO PYTHON  /  2026",
        "CITY": "LIBERTY BAY", "WANTED": "BUSCA:", "MISSION_DONE": "HECHO", "BAGS": "PAQUETES {count}/4",
        "CAR_SEDAN": "SEDAN", "CAR_COUPE": "COUPE", "CAR_TAXI": "TAXI", "CAR_SPORT": "DEPORTIVO", "CAR_COMPACT": "COMPACTO",
        "GARAGE": "GARAJE", "PHONE": "F: TELEFONO", "SCORE": "PUNTOS {score}  x{multiplier}",
        "WALKING": "A PIE", "NO_CAR": "NO HAY AUTO CERCA", "DRIVING": "AL VOLANTE",
        "CAR_STOLEN": "ROBO DE AUTO - BUSCADO!", "EMPTY_GUN": "SIN MUNICION", "NO_PHONE": "NO HAY TELEFONO CERCA",
        "JOB1_START": "TRABAJO ACEPTADO: RECOGE 4 PAQUETES", "JOB2_START": "NUEVO TRABAJO: LLEVA UN AUTO ROBADO AL GARAJE",
        "NO_MORE_JOBS": "NO HAY MAS TRABAJOS POR AHORA", "JOB1_ACTIVE": "TRABAJO: RECOGE LOS CUATRO PAQUETES",
        "JOB2_ACTIVE": "TRABAJO: LLEVA UN AUTO ROBADO", "BUSTED": "ARRESTADO - MULTIPLICADOR A LA MITAD",
        "HEAT_COOLING": "BAJA LA ALERTA", "ASSAULT": "AGRESION - BUSCADO!",
        "POLICE_ATTACK": "ATAQUE A LA POLICIA!", "HIT_AND_RUN": "ATROPELLO Y FUGA - BUSCADO!",
        "BAG_REWARD": "PAQUETE RECOGIDO +${amount}", "JOB_COMPLETE": "TRABAJO COMPLETADO!",
        "CAR_DELIVERED": "AUTO ENTREGADO - TRABAJO COMPLETADO", "STOLEN_CAR_REQUIRED": "EL GARAJE NECESITA UN AUTO ROBADO",
        "BRIBE_USED": "SOBORNO: ALERTA ELIMINADA", "AMMO_PICKUP": "PISTOLA: 6 BALAS", "CASH_PICKUP": "CAJA: +${amount}",
        "DISTRICT_ANNOUNCE": "BARRIO: {name}", "DISTRICT_CENTER": "CASCO ANTIGUO", "DISTRICT_UPTOWN": "ZONA ALTA",
        "DISTRICT_PORT": "LOS MUELLES", "DISTRICT_BAY": "BAHIA SUR", "MISSION_PHONE": "F  RESPONDER", "STEAL_CAR": "E  ROBAR AUTO",
        "EXIT_CAR": "E  BAJAR  /  {name}", "ENTER_CAR": "E  ROBAR AUTO", "CONTROLS": "WASD / FLECHAS",
        "PISTOL_AMMO": "PISTOLA {ammo}  ESPACIO", "RADIO_HINT": "R  RADIO", "RADIO_CHANGE": "RADIO: EMISORA {station}", "RADIO_ON_FOOT": "LA RADIO SOLO FUNCIONA EN EL AUTO",
        "PAUSED": "PAUSA", "RESUME": "ESC PARA SEGUIR", "MAIN_MENU": "ENTER PARA EL MENU",
    },
}


def load_settings():
    defaults = {"music": True, "sfx": True, "fullscreen": False, "language": "it"}
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        for key in ("music", "sfx", "fullscreen"):
            if key in data:
                defaults[key] = bool(data[key])
        if data.get("language") in TEXT:
            defaults["language"] = data["language"]
    except (OSError, ValueError, TypeError):
        pass
    return defaults


@lru_cache(maxsize=32)
def get_font(size):
    return pygame.font.Font(None, size)


class Audio:
    """Original synthesized soundtrack and effects; no external assets needed."""
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.ready = False
        self.music_on = enabled
        self.started = False
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.ready = True
            self.music_tracks = [self._make_music(station) for station in range(3)]
            self.station = 0
            self.click = self._tone(620, .045, .11)
            self.pickup = self._tone(880, .16, .12)
            self.siren = self._tone(740, .32, .1)
            self.weapon = self._tone(185, .075, .15)
        except pygame.error:
            self.ready = False

    @staticmethod
    def _tone(freq, duration, volume):
        rate = 22050
        samples = array("h")
        for i in range(int(rate * duration)):
            fade = min(1, i / 220, (rate * duration - i) / 1000)
            value = int(32767 * volume * max(0, fade) * math.sin(math.tau * freq * i / rate))
            samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    @staticmethod
    def _make_music(station=0):
        # Three original radio loops share a short chord-driven synth arrangement.
        rate, duration = 22050, 8.0
        root_sets = (
            (55.0, 73.42, 65.41, 49.0),
            (73.42, 82.41, 65.41, 98.0),
            (49.0, 55.0, 65.41, 73.42),
        )
        melodies = (
            (0, 7, 12, 7, 3, 7, 10, 7, 0, 7, 12, 15, 12, 7, 3, 7),
            (0, 3, 7, 10, 12, 10, 7, 3, 0, 7, 10, 14, 12, 7, 3, 0),
            (0, 5, 7, 12, 7, 5, 3, 5, 0, 5, 10, 12, 10, 7, 5, 3),
        )
        roots, melody = root_sets[station], melodies[station]
        beat_length = (.5, .4, .6)[station]
        samples = array("h")
        for i in range(int(rate * duration)):
            t = i / rate
            beat = int(t / beat_length)
            chord = roots[(beat // 4) % len(roots)]
            local_beat = t % beat_length
            bass = math.sin(math.tau * chord * t) * (0.15 + 0.08 * math.sin(math.tau * .5 * t))
            pad = (math.sin(math.tau * chord * 2 * t) + math.sin(math.tau * chord * 3 * t)) * .045
            note_id = int(t / (beat_length / 2)) % len(melody)
            note = chord * 4 * (2 ** (melody[note_id] / 12))
            pluck = math.sin(math.tau * note * t) * math.exp(-local_beat * 7) * .12
            drum = math.sin(math.tau * (72 - 30 * min(local_beat, .2) / .2) * local_beat) * math.exp(-local_beat * 20) * .13
            edge_fade = max(0, min(1, t / .02, (duration - t) / .02))
            value = max(-.7, min(.7, bass + pad + pluck + drum)) * edge_fade
            samples.append(int(value * 32767))
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def start_music(self):
        if self.ready and self.music_on and not self.started:
            self.started = True
            self.music_tracks[self.station].play(-1)

    def next_station(self):
        if not self.ready:
            return 0
        if self.started:
            pygame.mixer.stop()
            self.started = False
        self.station = (self.station + 1) % len(self.music_tracks)
        self.start_music()
        return self.station + 1

    def event(self, event):
        pass

    def sfx(self, which="click"):
        if self.ready and self.enabled:
            getattr(self, which, self.click).play()

    def set_music(self, enabled):
        self.music_on = enabled
        if enabled:
            self.started = False
            self.start_music()
        elif self.ready:
            pygame.mixer.stop()
            self.started = False


def text(surface, value, x, y, size=9, color=None, font=None):
    font = font or get_font(size)
    image = font.render(str(value), False, color or PALETTE["white"])
    surface.blit(image, (x, y))


def center_text(surface, value, y, size=9, color=None, font=None):
    font = font or get_font(size)
    image = font.render(str(value), False, color or PALETTE["white"])
    surface.blit(image, (W // 2 - image.get_width() // 2, y))


def draw_scanlines(surface, tick):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    for y in range(tick % 2, H, 3):
        pygame.draw.line(overlay, (0, 0, 0, 33), (0, y), (W, y))
    surface.blit(overlay, (0, 0))


class City:
    def __init__(self):
        self.width, self.height = 1600, 1200
        self.road = 112
        self.block = 240
        self.buildings = []
        self.windows = []
        for by in range(0, self.height, self.block + self.road):
            for bx in range(0, self.width, self.block + self.road):
                rect = pygame.Rect(bx + self.road + 9, by + self.road + 9, self.block - 18, self.block - 18)
                self.buildings.append(rect)
                rng = random.Random(bx * 7 + by * 13)
                for _ in range(18):
                    wx = rng.randrange(rect.left + 8, rect.right - 8)
                    wy = rng.randrange(rect.top + 8, rect.bottom - 8)
                    self.windows.append((wx, wy, rng.choice((0, 1))))

    def draw(self, target, camera):
        target.fill((29, 53, 59))
        ox, oy = -int(camera.x) % (self.block + self.road), -int(camera.y) % (self.block + self.road)
        for x in range(ox - 360, W + 360, self.block + self.road):
            pygame.draw.rect(target, (43, 48, 55), (x, 0, self.road, H))
            pygame.draw.line(target, (91, 89, 74), (x + self.road // 2, 0), (x + self.road // 2, H), 1)
        for y in range(oy - 360, H + 360, self.block + self.road):
            pygame.draw.rect(target, (43, 48, 55), (0, y, W, self.road))
            pygame.draw.line(target, (91, 89, 74), (0, y + self.road // 2), (W, y + self.road // 2), 1)
        view = pygame.Rect(int(camera.x) - 310, int(camera.y) - 310, W + 620, H + 620)
        for rect in self.buildings:
            if not rect.colliderect(view):
                continue
            r = rect.move(-int(camera.x), -int(camera.y))
            pygame.draw.rect(target, (18, 27, 35), r.move(4, 5))
            pygame.draw.rect(target, (76, 83, 82), r)
            pygame.draw.rect(target, (105, 109, 99), (r.x + 4, r.y + 4, r.w - 8, 5))
        for wx, wy, lit in self.windows:
            sx, sy = wx - camera.x, wy - camera.y
            if -3 < sx < W and -3 < sy < H:
                pygame.draw.rect(target, (165, 138, 89) if lit else (48, 64, 67), (int(sx), int(sy), 3, 4))
        # Road dashes create scale and direction without clutter.
        for x in range(ox - 360, W + 360, self.block + self.road):
            for yy in range(-24, H + 24, 24):
                pygame.draw.rect(target, (113, 105, 82), (x + self.road // 2, yy, 1, 8))
        for y in range(oy - 360, H + 360, self.block + self.road):
            for xx in range(-24, W + 24, 24):
                pygame.draw.rect(target, (113, 105, 82), (xx, y + self.road // 2, 8, 1))


class Actor:
    def __init__(self, x, y, coat):
        self.pos = pygame.Vector2(x, y)
        self.coat = coat
        self.vehicle = False
        self.heading = 0
        self.speed = 0.0
        self.vehicle_color = (224, 174, 74)
        self.vehicle_name = "BERLINA"
        self.stolen_vehicle = False
        self.weapon_ammo = 0

    def rect(self):
        if self.vehicle:
            return pygame.Rect(int(self.pos.x - 8), int(self.pos.y - 6), 16, 12)
        return pygame.Rect(int(self.pos.x - 4), int(self.pos.y - 5), 8, 10)

    @staticmethod
    def draw_car(surface, pos, camera, color, heading=0, police=False, tick=0):
        x, y = int(pos.x - camera.x), int(pos.y - camera.y)
        car = pygame.Surface((20, 11), pygame.SRCALPHA)
        pygame.draw.rect(car, (17, 22, 26), (0, 0, 20, 11), border_radius=2)
        pygame.draw.rect(car, color, (2, 1, 15, 9), border_radius=2)
        pygame.draw.rect(car, (37, 62, 72), (9, 2, 6, 7))
        if police:
            light = (238, 70, 75) if tick % 12 < 6 else (55, 133, 231)
            pygame.draw.rect(car, light, (8, 1, 5, 2))
        rotated = pygame.transform.rotate(car, -heading)
        surface.blit(rotated, rotated.get_rect(center=(x, y)))

    def draw(self, surface, camera):
        x, y = int(self.pos.x - camera.x), int(self.pos.y - camera.y)
        if self.vehicle:
            self.draw_car(surface, self.pos, camera, self.vehicle_color, self.heading)
        else:
            pygame.draw.ellipse(surface, (11, 19, 24), (x - 5, y + 3, 11, 5))
            pygame.draw.rect(surface, self.coat, (x - 3, y - 3, 7, 8))
            pygame.draw.rect(surface, (228, 181, 138), (x - 2, y - 6, 5, 4))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grand Theft Snake | SN Colors")
        self.settings = load_settings()
        flags = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        size = (0, 0) if self.settings["fullscreen"] else (W * SCALE, H * SCALE)
        self.window = pygame.display.set_mode(size, flags)
        self.canvas = pygame.Surface((W, H))
        self.clock = pygame.time.Clock()
        self.audio = Audio(self.settings["sfx"])
        self.audio.set_music(self.settings["music"])
        self.state = "intro"
        self.intro_time = 0
        self.tick = 0
        self.menu_items = ["NEW_GAME", "SETTINGS", "EXIT"]
        self.menu_index = 0
        self.option_index = 0
        self.character_index = 0
        self.load_time = 0
        self.money = 0
        self.message = ""
        self.message_time = 0
        self.city = City()
        self.player = None
        self.district = ""
        self.camera = pygame.Vector2()
        self.initial_pickups = [(56, 200), (1150, 200), (56, 760), (1112, 760)]
        self.initial_cars = [
            ((430, 56), (224, 174, 74), 90, "COUPÉ"),
            ((56, 430), (91, 151, 194), 0, "TAXI"),
            ((780, 408), (189, 91, 100), 90, "SPORTIVA"),
        ]
        self.pickups = []
        self.parked_cars = []
        self.traffic_cars = []
        self.police = []
        self.wanted = 0
        self.heat_timer = 0.0
        self.score = 0
        self.multiplier = 1
        self.mission_active = False
        self.mission_complete = False
        self.mission_stage = 0
        self.phones = []
        self.crates = []
        self.pedestrians = []
        self.projectiles = []
        self.running = True

    def t(self, key):
        return TEXT[self.settings["language"]].get(key, key)

    def save_settings(self):
        try:
            SAVE_FILE.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")
        except OSError:
            pass

    def toggle_fullscreen(self):
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        flags = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        size = (0, 0) if self.settings["fullscreen"] else (W * SCALE, H * SCALE)
        self.window = pygame.display.set_mode(size, flags)
        self.save_settings()

    def key(self, key):
        if key == pygame.K_F11:
            self.toggle_fullscreen()
            return
        if self.state == "intro":
            if key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.state = "menu"
                self.audio.sfx()
        elif self.state == "menu":
            if key in (pygame.K_UP, pygame.K_w):
                self.menu_index = (self.menu_index - 1) % len(self.menu_items); self.audio.sfx()
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.menu_index = (self.menu_index + 1) % len(self.menu_items); self.audio.sfx()
            elif key == pygame.K_RETURN:
                self.audio.sfx()
                if self.menu_index == 0: self.state = "character"
                elif self.menu_index == 1: self.state = "settings"
                else: self.running = False
            elif key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == "settings":
            if key in (pygame.K_UP, pygame.K_w): self.option_index = (self.option_index - 1) % 4; self.audio.sfx()
            elif key in (pygame.K_DOWN, pygame.K_s): self.option_index = (self.option_index + 1) % 4; self.audio.sfx()
            elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
                if self.option_index == 0:
                    self.settings["music"] = not self.settings["music"]; self.audio.set_music(self.settings["music"])
                elif self.option_index == 1:
                    self.settings["sfx"] = not self.settings["sfx"]; self.audio.enabled = self.settings["sfx"]
                elif self.option_index == 2: self.toggle_fullscreen()
                else:
                    languages = ("it", "en", "fr", "es")
                    delta = -1 if key == pygame.K_LEFT else 1
                    current = languages.index(self.settings["language"])
                    self.settings["language"] = languages[(current + delta) % len(languages)]
                    self.message = ""
                self.save_settings(); self.audio.sfx()
            elif key == pygame.K_ESCAPE:
                self.state = "menu"
        elif self.state == "character":
            if key in (pygame.K_LEFT, pygame.K_a):
                self.character_index = (self.character_index - 1) % len(CHARACTERS); self.audio.sfx()
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.character_index = (self.character_index + 1) % len(CHARACTERS); self.audio.sfx()
            elif key == pygame.K_RETURN:
                self.state = "loading"; self.load_time = 0; self.audio.sfx()
            elif key == pygame.K_ESCAPE: self.state = "menu"
        elif self.state == "loading":
            if key == pygame.K_ESCAPE: self.state = "character"
        elif self.state == "game":
            if key == pygame.K_ESCAPE: self.state = "pause"
            elif key == pygame.K_e: self.toggle_vehicle()
            elif key == pygame.K_f: self.use_phone()
            elif key == pygame.K_SPACE: self.fire_weapon()
            elif key == pygame.K_r: self.change_radio()
        elif self.state == "pause":
            if key == pygame.K_ESCAPE: self.state = "game"
            elif key == pygame.K_RETURN: self.state = "menu"

    def toggle_vehicle(self):
        if not self.player: return
        self.message_time = 1.3
        if self.player.vehicle:
            p = self.player
            direction = pygame.Vector2(math.cos(math.radians(p.heading)), math.sin(math.radians(p.heading)))
            p.pos += pygame.Vector2(-direction.y, direction.x) * 17
            p.vehicle = False
            self.parked_cars.append({
                "pos": p.pos.copy(), "color": p.vehicle_color, "heading": p.heading,
                "name": p.vehicle_name, "stolen": p.stolen_vehicle,
            })
            self.message = self.t("WALKING")
        else:
            available = [("parked", car) for car in self.parked_cars] + [("traffic", car) for car in self.traffic_cars]
            choice = min(available, key=lambda item: self.player.pos.distance_to(item[1]["pos"]), default=None)
            if choice is None or self.player.pos.distance_to(choice[1]["pos"]) > 25:
                self.message = self.t("NO_CAR")
                self.message_time = 1.0
                return
            kind, closest = choice
            self.player.pos = closest["pos"].copy()
            self.player.heading = closest["heading"]
            self.player.vehicle_color = closest["color"]
            self.player.vehicle_name = closest.get("name", "BERLINA")
            self.player.stolen_vehicle = closest.get("stolen", False)
            self.player.speed = abs(closest.get("speed", 0))
            (self.parked_cars if kind == "parked" else self.traffic_cars).remove(closest)
            self.player.vehicle = True
            if not self.player.stolen_vehicle:
                self.player.stolen_vehicle = True
                self.commit_car_theft()
            else:
                self.message = self.t("DRIVING")
        self.player.speed = 0
        self.audio.sfx()

    def commit_car_theft(self):
        self.score += 500 * self.multiplier
        self.message = self.t("CAR_STOLEN")
        self.message_time = 2.2
        self.raise_wanted(1)

    def raise_wanted(self, amount, reason=""):
        self.wanted = min(5, self.wanted + amount)
        self.heat_timer = 0
        self.update_police_count()
        self.audio.sfx("siren")
        if reason:
            self.message = self.t(reason)
            self.message_time = 2.0

    def fire_weapon(self):
        if self.player.weapon_ammo <= 0:
            self.message = self.t("EMPTY_GUN")
            self.message_time = 1.0
            return
        angle = math.radians(self.player.heading)
        direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.projectiles.append({"pos": self.player.pos + direction * 12, "dir": direction, "life": .8})
        self.player.weapon_ammo -= 1
        self.audio.sfx("weapon")

    def change_radio(self):
        if not self.player.vehicle:
            self.message = self.t("RADIO_ON_FOOT")
            self.message_time = 1.2
            return
        station = self.audio.next_station()
        self.message = self.t("RADIO_CHANGE").format(station=station)
        self.message_time = 1.2

    def use_phone(self):
        phone = min(self.phones, key=lambda item: self.player.pos.distance_to(item), default=None)
        if phone is None or self.player.pos.distance_to(phone) > 30:
            self.message = self.t("NO_PHONE")
            self.message_time = 1.2
            return
        if self.mission_stage == 0:
            self.mission_stage = 1
            self.mission_active = True
            self.message = self.t("JOB1_START")
            self.audio.sfx("pickup")
        elif self.mission_stage == 1 and self.mission_complete:
            self.mission_stage = 2
            self.mission_complete = False
            self.message = self.t("JOB2_START")
            self.audio.sfx("pickup")
        elif self.mission_complete:
            self.message = self.t("NO_MORE_JOBS")
        elif self.mission_stage == 1:
            self.message = self.t("JOB1_ACTIVE")
        else:
            self.message = self.t("JOB2_ACTIVE")
        self.message_time = 2.2

    def start_game(self):
        self.money = 0
        self.score = 0
        self.multiplier = 1
        self.wanted = 0
        self.heat_timer = 0
        self.police = []
        self.mission_active = False
        self.mission_complete = False
        self.mission_stage = 0
        self.pickups = [pygame.Vector2(x, y) for x, y in self.initial_pickups]
        self.parked_cars = [
            {"pos": pygame.Vector2(x, y), "color": color, "heading": heading, "name": name, "stolen": False}
            for (x, y), color, heading, name in self.initial_cars
        ]
        self.traffic_cars = [
            {"pos": pygame.Vector2(130, 20), "color": (111, 156, 133), "speed": 35, "heading": 0, "name": "COMPACT", "stolen": False},
            {"pos": pygame.Vector2(820, 96), "color": (168, 111, 174), "speed": -29, "heading": 180, "name": "TAXI", "stolen": False},
            {"pos": pygame.Vector2(1380, 20), "color": (103, 132, 191), "speed": -42, "heading": 180, "name": "SPORTIVA", "stolen": False},
        ]
        self.phones = [pygame.Vector2(392, 78), pygame.Vector2(1112, 408), pygame.Vector2(56, 760)]
        self.crates = [
            {"pos": pygame.Vector2(760, 56), "kind": "bribe"},
            {"pos": pygame.Vector2(1464, 760), "kind": "cash"},
            {"pos": pygame.Vector2(56, 408), "kind": "ammo"},
        ]
        self.pedestrians = [
            {"pos": pygame.Vector2(56, 280), "dir": 1, "color": (201, 161, 117)},
            {"pos": pygame.Vector2(408, 610), "dir": -1, "color": (133, 176, 155)},
            {"pos": pygame.Vector2(760, 200), "dir": 1, "color": (189, 129, 160)},
            {"pos": pygame.Vector2(1112, 890), "dir": -1, "color": (143, 164, 202)},
            {"pos": pygame.Vector2(1464, 340), "dir": 1, "color": (210, 188, 116)},
        ]
        self.projectiles = []
        self.player = Actor(392, 56, CHARACTERS[self.character_index]["coat"])
        self.player.stolen_vehicle = False
        self.district = self.district_at(self.player.pos)
        self.camera.update(self.player.pos.x - W / 2, self.player.pos.y - H / 2)
        self.state = "game"

    @staticmethod
    def nearest_road_node(pos):
        ix = max(0, min(4, round((pos.x - 56) / 352)))
        iy = max(0, min(3, round((pos.y - 56) / 352)))
        return ix, iy

    @staticmethod
    def road_target(pos):
        ix, iy = Game.nearest_road_node(pos)
        road_x, road_y = 56 + ix * 352, 56 + iy * 352
        if abs(pos.x - road_x) <= 56:
            return pygame.Vector2(road_x, pos.y)
        if abs(pos.y - road_y) <= 56:
            return pygame.Vector2(pos.x, road_y)
        return pygame.Vector2(road_x, road_y)

    def police_route(self, start, target):
        ix, iy = self.nearest_road_node(start)
        tx, ty = self.nearest_road_node(target)
        route = []
        while ix != tx:
            ix += 1 if tx > ix else -1
            route.append(pygame.Vector2(56 + ix * 352, 56 + iy * 352))
        while iy != ty:
            iy += 1 if ty > iy else -1
            route.append(pygame.Vector2(56 + ix * 352, 56 + iy * 352))
        if not route or route[-1].distance_to(target) > 2:
            route.append(target.copy())
        return route

    def update_police_count(self):
        wanted_count = min(3, 1 + (self.wanted - 1) // 2) if self.wanted else 0
        self.police = self.police[:wanted_count]
        if not self.player:
            return
        candidates = []
        for iy in range(4):
            for ix in range(5):
                node = pygame.Vector2(56 + ix * 352, 56 + iy * 352)
                distance = node.distance_to(self.player.pos)
                if distance > 270 and all(cop["pos"].distance_to(node) > 120 for cop in self.police):
                    candidates.append((distance, node))
        candidates.sort(key=lambda item: item[0])
        while len(self.police) < wanted_count and candidates:
            _, node = candidates.pop(0)
            self.police.append({"pos": node, "heading": 0, "route": [], "color": (226, 228, 224)})
            self.audio.sfx("siren")

    def move_police(self, dt):
        for cop in self.police:
            if not cop["route"]:
                target = self.road_target(self.player.pos)
                cop["route"] = self.police_route(cop["pos"], target)
            if not cop["route"]:
                continue
            waypoint = cop["route"][0]
            delta = waypoint - cop["pos"]
            distance = delta.length()
            step = 91 * dt
            if distance <= step:
                cop["pos"] = waypoint.copy()
                cop["route"].pop(0)
            elif distance:
                direction = delta / distance
                cop["pos"] += direction * step
                cop["heading"] = math.degrees(math.atan2(direction.y, direction.x))

    def arrest_player(self):
        self.multiplier = max(1, self.multiplier // 2)
        self.police.clear()
        self.wanted = 0
        self.heat_timer = 0
        self.player.vehicle = False
        self.player.stolen_vehicle = False
        self.player.speed = 0
        self.player.weapon_ammo = 0
        self.player.pos.update(56, 56)
        self.camera.update(self.player.pos.x - W / 2, self.player.pos.y - H / 2)
        self.district = self.district_at(self.player.pos)
        self.message = self.t("BUSTED")
        self.message_time = 2.5

    def update_wanted(self, dt):
        if not self.wanted:
            return
        distance = min((cop["pos"].distance_to(self.player.pos) for cop in self.police), default=9999)
        if distance > 320:
            self.heat_timer += dt
        else:
            self.heat_timer = 0
        if distance < 17:
            self.arrest_player()
        elif self.heat_timer >= 9:
            self.wanted = max(0, self.wanted - 1)
            self.heat_timer = 0
            self.message = self.t("HEAT_COOLING")
            self.message_time = 1.5
            self.update_police_count()

    @staticmethod
    def district_at(pos):
        west, north = pos.x < 800, pos.y < 600
        if west and north: return "DISTRICT_CENTER"
        if not west and north: return "DISTRICT_UPTOWN"
        if west: return "DISTRICT_PORT"
        return "DISTRICT_BAY"

    def move_traffic(self, dt):
        for car in self.traffic_cars:
            car["pos"].x += car["speed"] * dt
            if car["speed"] > 0 and car["pos"].x > self.city.width + 12:
                car["pos"].x = -12
            elif car["speed"] < 0 and car["pos"].x < -12:
                car["pos"].x = self.city.width + 12
        for pedestrian in self.pedestrians:
            pedestrian["pos"].y += pedestrian["dir"] * 24 * dt
            if pedestrian["pos"].y < 18 or pedestrian["pos"].y > self.city.height - 18:
                pedestrian["dir"] *= -1

    def move_projectiles(self, dt):
        for shot in self.projectiles[:]:
            shot["pos"] += shot["dir"] * 270 * dt
            shot["life"] -= dt
            pedestrian = next((person for person in self.pedestrians if person["pos"].distance_to(shot["pos"]) < 8), None)
            if pedestrian:
                self.pedestrians.remove(pedestrian)
                self.projectiles.remove(shot)
                self.score += 100 * self.multiplier
                self.raise_wanted(2, "ASSAULT")
                continue
            cop = next((officer for officer in self.police if officer["pos"].distance_to(shot["pos"]) < 12), None)
            if cop:
                self.police.remove(cop)
                self.projectiles.remove(shot)
                self.score += 1000 * self.multiplier
                self.raise_wanted(1, "POLICE_ATTACK")
                continue
            if shot["life"] <= 0 or not (0 <= shot["pos"].x <= self.city.width and 0 <= shot["pos"].y <= self.city.height):
                self.projectiles.remove(shot)

    def move_player(self, dt, keys):
        p = self.player
        dx = float(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - float(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = float(keys[pygame.K_s] or keys[pygame.K_DOWN]) - float(keys[pygame.K_w] or keys[pygame.K_UP])
        if p.vehicle:
            if dx: p.heading = (p.heading + dx * 130 * dt * (1 if p.speed >= 0 else -1)) % 360
            p.speed += (-dy * 165 - p.speed * 1.2) * dt
            p.speed = max(-75, min(150, p.speed))
            direction = pygame.Vector2(math.cos(math.radians(p.heading)), math.sin(math.radians(p.heading)))
            movement = direction * p.speed * dt
        else:
            movement = pygame.Vector2(dx, dy)
            if movement.length_squared():
                p.heading = math.degrees(math.atan2(movement.y, movement.x))
                movement = movement.normalize() * 83 * dt
        old = p.pos.copy()
        p.pos.x = max(8, min(self.city.width - 8, p.pos.x + movement.x))
        if any(p.rect().colliderect(b) for b in self.city.buildings): p.pos.x = old.x
        p.pos.y = max(8, min(self.city.height - 8, p.pos.y + movement.y))
        if any(p.rect().colliderect(b) for b in self.city.buildings): p.pos.y = old.y
        if p.vehicle:
            hit = next((person for person in self.pedestrians if person["pos"].distance_to(p.pos) < 12), None)
            if hit:
                self.pedestrians.remove(hit)
                self.score += 100 * self.multiplier
                self.raise_wanted(2, "HIT_AND_RUN")
        if self.mission_active and self.mission_stage == 1 and not self.mission_complete:
            for pickup in self.pickups[:]:
                if p.pos.distance_to(pickup) < 15:
                    self.pickups.remove(pickup)
                    self.money += 100 * self.multiplier
                    self.score += 1000 * self.multiplier
                    self.audio.sfx("pickup")
                    if self.pickups:
                        self.message = self.t("BAG_REWARD").format(amount=100 * self.multiplier)
                        self.message_time = 1.5
                    else:
                        self.mission_complete = True
                        self.money += 500 * self.multiplier
                        self.score += 5000 * self.multiplier
                        self.multiplier = min(5, self.multiplier + 1)
                        self.message = self.t("JOB_COMPLETE")
                        self.message_time = 2.5
        if self.mission_active and self.mission_stage == 2 and not self.mission_complete:
            depot = pygame.Vector2(1464, 1112)
            if p.pos.distance_to(depot) < 24:
                if p.vehicle and p.stolen_vehicle:
                    self.mission_complete = True
                    self.money += 1000 * self.multiplier
                    self.score += 5000 * self.multiplier
                    self.multiplier = min(5, self.multiplier + 1)
                    self.message = self.t("CAR_DELIVERED")
                    self.message_time = 2.5
                else:
                    self.message = self.t("STOLEN_CAR_REQUIRED")
                    self.message_time = 1.5
        for crate in self.crates[:]:
            if p.pos.distance_to(crate["pos"]) < 14:
                self.crates.remove(crate)
                if crate["kind"] == "bribe":
                    self.wanted = 0
                    self.police.clear()
                    self.heat_timer = 0
                    self.message = self.t("BRIBE_USED")
                elif crate["kind"] == "ammo":
                    self.player.weapon_ammo += 6
                    self.message = self.t("AMMO_PICKUP")
                else:
                    self.money += 250 * self.multiplier
                    self.score += 2000 * self.multiplier
                    self.message = self.t("CASH_PICKUP").format(amount=250 * self.multiplier)
                self.audio.sfx("pickup")
                self.message_time = 2.0
        new_district = self.district_at(p.pos)
        if new_district != self.district:
            self.district = new_district
            self.message = self.t("DISTRICT_ANNOUNCE").format(name=self.t(self.district))
            self.message_time = 1.8
        target = p.pos - pygame.Vector2(W / 2, H / 2)
        self.camera += (target - self.camera) * min(1, 5 * dt)
        self.camera.x = max(0, min(self.city.width - W, self.camera.x))
        self.camera.y = max(0, min(self.city.height - H, self.camera.y))
        if self.message_time > 0: self.message_time -= dt

    def draw_logo(self, publisher, y, progress):
        # A wholly original animated emblem, drawn at runtime as a short ident.
        cx = W // 2; radius = int(12 + 4 * math.sin(self.tick / 9))
        pygame.draw.circle(self.canvas, (20, 38, 46), (cx, y), radius + 8)
        pygame.draw.circle(self.canvas, PALETTE["mint"] if publisher else PALETTE["amber"], (cx, y), radius, 2)
        pygame.draw.line(self.canvas, PALETTE["white"], (cx - 5, y), (cx + 5, y), 2)
        pygame.draw.line(self.canvas, PALETTE["white"], (cx, y - 5), (cx, y + 5), 2)
        center_text(self.canvas, "SN COLORS" if publisher else "SN COLORS STUDIO", y + 21, 17 if publisher else 15, PALETTE["white"])
        center_text(self.canvas, self.t("PUBLISHER" if publisher else "CREATED_BY"), y + 42, 8, PALETTE["muted"])
        pygame.draw.rect(self.canvas, (45, 58, 62), (W // 2 - 45, H - 28, 90, 2))
        pygame.draw.rect(self.canvas, PALETTE["mint"], (W // 2 - 45, H - 28, int(90 * progress), 2))

    def draw_minimap(self):
        x, y, mw, mh = 419, 33, 49, 37
        pygame.draw.rect(self.canvas, (8, 14, 19), (x - 2, y - 2, mw + 4, mh + 4))
        pygame.draw.rect(self.canvas, (28, 48, 49), (x, y, mw, mh))
        sx, sy = mw / self.city.width, mh / self.city.height
        spacing = (self.city.block + self.city.road)
        for world_x in range(0, self.city.width, spacing):
            pygame.draw.rect(self.canvas, (63, 67, 68), (x + int(world_x * sx), y, max(2, int(self.city.road * sx)), mh))
        for world_y in range(0, self.city.height, spacing):
            pygame.draw.rect(self.canvas, (63, 67, 68), (x, y + int(world_y * sy), mw, max(2, int(self.city.road * sy))))
        for pickup in self.pickups:
            pygame.draw.circle(self.canvas, PALETTE["amber"], (int(x + pickup.x * sx), int(y + pickup.y * sy)), 1)
        for phone in self.phones:
            pygame.draw.circle(self.canvas, (123, 164, 232), (int(x + phone.x * sx), int(y + phone.y * sy)), 1)
        for crate in self.crates:
            pygame.draw.circle(self.canvas, (109, 226, 216), (int(x + crate["pos"].x * sx), int(y + crate["pos"].y * sy)), 1)
        if self.mission_active and self.mission_stage == 2 and not self.mission_complete:
            pygame.draw.circle(self.canvas, PALETTE["mint"], (int(x + 1464 * sx), int(y + 1112 * sy)), 2)
        for cop in self.police:
            pygame.draw.circle(self.canvas, PALETTE["red"], (int(x + cop["pos"].x * sx), int(y + cop["pos"].y * sy)), 1)
        for pedestrian in self.pedestrians:
            pygame.draw.circle(self.canvas, (198, 202, 181), (int(x + pedestrian["pos"].x * sx), int(y + pedestrian["pos"].y * sy)), 1)
        px, py = int(x + self.player.pos.x * sx), int(y + self.player.pos.y * sy)
        pygame.draw.circle(self.canvas, PALETTE["mint"], (px, py), 2)

    def draw(self):
        c = self.canvas
        c.fill(PALETTE["ink"])
        if self.state == "intro":
            center = 0 if self.intro_time < 2.1 else 1
            local = self.intro_time if center == 0 else self.intro_time - 2.1
            self.draw_logo(center == 0, 104, min(1, local / 1.8))
            if self.intro_time > 4.0: center_text(c, self.t("PRESS_KEY"), H - 16, 8, PALETTE["muted"])
        elif self.state == "menu":
            # Nighttime city silhouette and diagonal neon band.
            for x in range(0, W, 32):
                h = 35 + ((x * 7) % 49)
                pygame.draw.rect(c, (17, 31, 39), (x, 155 - h, 27, h))
                pygame.draw.line(c, (31, 49, 54), (x, 155 - h), (x + 27, 155 - h), 1)
            pygame.draw.rect(c, (12, 17, 24), (0, 154, W, 116))
            text(c, self.t("PRESENTS"), 20, 18, 9, PALETTE["mint"])
            text(c, "GRAND THEFT", 20, 44, 33, PALETTE["white"])
            text(c, "SNAKE", 20, 72, 40, PALETTE["amber"])
            text(c, self.t("SLOGAN"), 22, 119, 9, PALETTE["muted"])
            for i, label in enumerate(self.menu_items):
                y = 175 + i * 21
                color = PALETTE["mint"] if i == self.menu_index else PALETTE["white"]
                if i == self.menu_index: text(c, ">", 22, y, 14, PALETTE["amber"])
                text(c, self.t(label), 36, y + 2, 13, color)
            text(c, self.t("PROTOTYPE"), 300, 250, 8, PALETTE["muted"])
        elif self.state == "settings":
            text(c, self.t("SETTINGS"), 30, 28, 25, PALETTE["mint"])
            options = [("MUSIC", self.settings["music"]), ("SFX", self.settings["sfx"]), ("FULLSCREEN", self.settings["fullscreen"]), ("LANGUAGE", self.settings["language"])]
            for i, (label, on) in enumerate(options):
                y = 92 + i * 29
                text(c, ">" if i == self.option_index else " ", 34, y, 14, PALETTE["amber"])
                text(c, self.t(label), 53, y + 2, 13, PALETTE["white"])
                language_key = {"it": "ITALIAN", "en": "ENGLISH", "fr": "FRENCH", "es": "SPANISH"}.get(on, "ENGLISH")
                value = self.t(language_key) if i == 3 else self.t("ON" if on else "OFF")
                text(c, value, 196, y + 2, 13, PALETTE["mint"] if on else PALETTE["muted"])
            text(c, self.t("CHANGE_SETTING"), 30, 207, 9, PALETTE["muted"])
            text(c, self.t("BACK"), 30, 239, 9, PALETTE["amber"])
        elif self.state == "character":
            text(c, self.t("CHOOSE_CHARACTER"), 30, 24, 20, PALETTE["mint"])
            ch = CHARACTERS[self.character_index]
            pygame.draw.rect(c, (21, 35, 43), (151, 73, 178, 125))
            pygame.draw.rect(c, ch["coat"], (229, 94, 22, 43))
            pygame.draw.rect(c, ch["skin"], (234, 79, 13, 16))
            pygame.draw.rect(c, (35, 43, 50), (221, 136, 12, 41))
            pygame.draw.rect(c, (35, 43, 50), (247, 136, 12, 41))
            text(c, "<", 174, 127, 24, PALETTE["amber"])
            text(c, ">", 301, 127, 24, PALETTE["amber"])
            center_text(c, ch["name"], 183, 20, PALETTE["white"])
            center_text(c, self.t(ch["tag"]), 206, 10, PALETTE["muted"])
            center_text(c, self.t("CHARACTER_CONTROLS"), 244, 8, PALETTE["amber"])
        elif self.state == "loading":
            center_text(c, self.t("LOADING"), 84, 18, PALETTE["white"])
            center_text(c, self.t("PREPARING_CITY"), 116, 9, PALETTE["muted"])
            center_text(c, self.t("FIND_PHONE"), 132, 9, PALETTE["amber"])
            pygame.draw.rect(c, (44, 58, 63), (90, 151, 300, 8))
            pygame.draw.rect(c, PALETTE["mint"], (92, 153, int(296 * min(1, self.load_time / 1.5)), 4))
            center_text(c, "SN COLORS", 205, 10, PALETTE["mint"])
        elif self.state in ("game", "pause"):
            self.city.draw(c, self.camera)
            for phone in self.phones:
                x, y = int(phone.x - self.camera.x), int(phone.y - self.camera.y)
                pulse = 4 + (self.tick // 12) % 3
                pygame.draw.circle(c, (82, 119, 179), (x, y), pulse, 1)
                pygame.draw.rect(c, (134, 176, 237), (x - 2, y - 4, 4, 7))
                pygame.draw.rect(c, (40, 60, 86), (x - 3, y + 3, 6, 2))
            for crate in self.crates:
                x, y = int(crate["pos"].x - self.camera.x), int(crate["pos"].y - self.camera.y)
                color = (112, 222, 207) if crate["kind"] == "bribe" else ((225, 99, 102) if crate["kind"] == "ammo" else (221, 168, 88))
                pygame.draw.rect(c, (29, 37, 39), (x - 6, y - 5, 12, 10))
                pygame.draw.rect(c, color, (x - 5, y - 4, 10, 8), 1)
                pygame.draw.line(c, color, (x - 5, y), (x + 5, y), 1)
            if self.mission_active and self.mission_stage == 2 and not self.mission_complete:
                depot_x, depot_y = 1464 - self.camera.x, 1112 - self.camera.y
                pygame.draw.circle(c, PALETTE["mint"], (int(depot_x), int(depot_y)), 13, 1)
                pygame.draw.polygon(c, PALETTE["mint"], [(int(depot_x), int(depot_y - 5)), (int(depot_x - 4), int(depot_y + 3)), (int(depot_x + 4), int(depot_y + 3))])
            for cop in self.police:
                Actor.draw_car(c, cop["pos"], self.camera, cop["color"], cop["heading"], True, self.tick)
            for car in self.traffic_cars:
                Actor.draw_car(c, car["pos"], self.camera, car["color"], car["heading"])
            for car in self.parked_cars:
                Actor.draw_car(c, car["pos"], self.camera, car["color"], car["heading"])
            for pedestrian in self.pedestrians:
                x, y = int(pedestrian["pos"].x - self.camera.x), int(pedestrian["pos"].y - self.camera.y)
                pygame.draw.ellipse(c, (10, 17, 19), (x - 4, y + 3, 9, 4))
                pygame.draw.rect(c, pedestrian["color"], (x - 2, y - 2, 5, 7))
                pygame.draw.rect(c, (221, 184, 146), (x - 1, y - 5, 3, 3))
            for shot in self.projectiles:
                x, y = int(shot["pos"].x - self.camera.x), int(shot["pos"].y - self.camera.y)
                pygame.draw.circle(c, (255, 242, 157), (x, y), 2)
            for pickup in self.pickups:
                x, y = int(pickup.x - self.camera.x), int(pickup.y - self.camera.y)
                pygame.draw.circle(c, (255, 190, 87), (x, y), 5)
                pygame.draw.circle(c, (255, 235, 160), (x, y), 2)
            self.player.draw(c, self.camera)
            self.draw_minimap()
            pygame.draw.rect(c, (9, 14, 21), (0, 0, W, 24))
            text(c, self.t("CITY"), 9, 7, 10, PALETTE["mint"])
            text(c, self.t(self.district), 9, 16, 7, PALETTE["muted"])
            text(c, self.t("WANTED"), 168, 6, 8, PALETTE["white"])
            for i in range(5):
                cx, cy = 198 + i * 9, 11
                points = []
                for j in range(10):
                    angle = -math.pi / 2 + j * math.pi / 5
                    radius = 4 if j % 2 == 0 else 2
                    points.append((int(cx + math.cos(angle) * radius), int(cy + math.sin(angle) * radius)))
                pygame.draw.polygon(c, PALETTE["amber"] if i < self.wanted else (71, 78, 85), points)
            if self.mission_active and self.mission_stage == 1 and self.pickups:
                arrow_target = min(self.pickups, key=lambda goal: self.player.pos.distance_to(goal))
            elif self.mission_active and self.mission_stage == 2 and not self.mission_complete:
                arrow_target = pygame.Vector2(1464, 1112)
            else:
                arrow_target = min(self.phones, key=lambda goal: self.player.pos.distance_to(goal), default=None)
            if arrow_target is not None:
                direction = arrow_target - self.player.pos
                if direction.length_squared():
                    direction = direction.normalize()
                    perpendicular = pygame.Vector2(-direction.y, direction.x)
                    origin = pygame.Vector2(244, 11)
                    arrow_points = [origin + direction * 4, origin - direction * 3 + perpendicular * 3, origin - direction * 3 - perpendicular * 3]
                    pygame.draw.polygon(c, PALETTE["amber"], [(round(point.x), round(point.y)) for point in arrow_points])
            if self.mission_complete:
                mission_label = self.t("MISSION_DONE")
            elif self.mission_active and self.mission_stage == 1:
                mission_label = self.t("BAGS").format(count=4 - len(self.pickups))
            elif self.mission_active and self.mission_stage == 2:
                mission_label = self.t("GARAGE")
            else:
                mission_label = self.t("PHONE")
            text(c, mission_label, 252, 6, 8, PALETTE["white"])
            text(c, f"${self.money:05d}", 387, 7, 10, PALETTE["amber"])
            text(c, self.t("SCORE").format(score=self.score, multiplier=self.multiplier), 240, 16, 7, PALETTE["muted"])
            if self.player.vehicle:
                car_name = self.t(VEHICLE_NAME_KEYS.get(self.player.vehicle_name, "CAR_SEDAN"))
                prompt = self.t("EXIT_CAR").format(name=car_name)
            else:
                near_car = any(self.player.pos.distance_to(car["pos"]) < 25 for car in self.parked_cars + self.traffic_cars)
                near_phone = any(self.player.pos.distance_to(phone) < 30 for phone in self.phones)
                prompt = self.t("ENTER_CAR") if near_car else (self.t("MISSION_PHONE") if near_phone else "")
            text(c, prompt, 9, H - 16, 9, PALETTE["amber"])
            text(c, self.t("CONTROLS"), 170, H - 16, 7, PALETTE["muted"])
            if self.player.vehicle:
                text(c, self.t("RADIO_HINT"), 270, H - 16, 7, PALETTE["muted"])
            if self.player.weapon_ammo:
                text(c, self.t("PISTOL_AMMO").format(ammo=self.player.weapon_ammo), 350, H - 16, 7, PALETTE["amber"])
            if self.message_time > 0:
                center_text(c, self.message, 38, 13, PALETTE["amber"])
            if self.state == "pause":
                shade = pygame.Surface((W, H), pygame.SRCALPHA); shade.fill((2, 5, 10, 190)); c.blit(shade, (0, 0))
                center_text(c, self.t("PAUSED"), 94, 29, PALETTE["mint"])
                center_text(c, self.t("RESUME"), 139, 11, PALETTE["white"])
                center_text(c, self.t("MAIN_MENU"), 157, 9, PALETTE["muted"])
        draw_scanlines(c, self.tick)

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, .05)
            self.tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.KEYDOWN: self.key(event.key)
                self.audio.event(event)
            if self.state == "intro":
                self.intro_time += dt
                if self.intro_time > 5.2: self.state = "menu"
            elif self.state == "loading":
                self.load_time += dt
                if self.load_time >= 1.5: self.start_game()
            elif self.state == "game":
                self.move_traffic(dt)
                self.move_player(dt, pygame.key.get_pressed())
                self.move_projectiles(dt)
                self.move_police(dt)
                self.update_wanted(dt)
            self.draw()
            screen_w, screen_h = self.window.get_size()
            scale = min(screen_w / W, screen_h / H)
            draw_w, draw_h = int(W * scale), int(H * scale)
            scaled = pygame.transform.scale(self.canvas, (draw_w, draw_h))
            self.window.fill(PALETTE["ink"])
            self.window.blit(scaled, ((screen_w - draw_w) // 2, (screen_h - draw_h) // 2))
            pygame.display.flip()
        self.save_settings()
        pygame.quit()


if __name__ == "__main__":
    try:
        Game().run()
    except pygame.error as exc:
        print(f"Impossibile avviare la finestra grafica: {exc}", file=sys.stderr)
