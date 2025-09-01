const routineWeights = {
    "sequence routine": {
        "small jump": {
            "scale": {
                "major": 80,
                "minor": 60,
                "harmonicMinor": 50,
                "melodicMinor": 20
            },
            "harmonic pattern": {
                "baker": 80,
                "repeated root": 40,
                "9th": 40,
                "remington modes": 30,
                "5th pedal": 50,
                "root pedal": 40,
                "thirds scale": 60,
                "triad scale": 30,
                "7th chord scale": 20,
                "octave scale": 40,
                "clarke 2nd study": 40,
                "1,1,-1": 10,
                "1,1,1,-2": 20,
                "1,-1,-1,-2": 5,
                "-1,-1,1,-2": 5,
                "-2,2,1": 5,
                "2,-2,-1": 5,
                "2,2,-2-1": 5,
                "-2,2,2,-1": 5
            }
        },
        "big jump": {
            "scale": {
                "major": 80,
                "minor": 70,
                "harmonic": 70,
                "fixed": 50
            },
            "harmonic pattern": {
                "1": 30,
                "baker": 70,
                "9th": 50,
                "repeated root": 30,
                "5th pedal": 40,
                "root pedal": 50,
                "skips": 30,
                "octaves": 50,
                "alberti": 40,
                "1,1,-1,-1": 10,
                "1,-1": 20,
                "1,1,-1": 10,
                "1,1,-2": 10,
                "1,1,1,-2": 10,
                "1,-1,-1,-2": 5,
                "-1,-1,1,-2": 5,
                "-1,1,-1,2": 10,
                "2,1,-2,-1": 5,
                "2,1,-1,-2": 5,
                "1,2,-1,-2": 5,
                "-1,2": 10,
                "2,-1,1,-1": 10,
                "-2,2,1": 5,
                "2,-2,1": 5,
                "2,2,-2,-1": 5,
                "-2,2,2,-1": 5,
                "2,-2,2,-1": 10,
                "2,2,-2,-2": 10,
                "2,-2": 10
            }
        },
        "dynamic pattern": {
            "speed": {
                "subito": 60,
                "gradual": 80
            },
            "blocks": {
                "1": 90,
                "2": 80,
                "4": 70,
                "8": 50,
                "16": 20
            },
            "dynamics": {
                "mf": 80,
                "p": 60,
                "f": 60,
                "pp": 40,
                "ff": 40
            }
        },
        "articulation pattern": {
            "t": 90,
            "ts": 40,
            "tts": 50,
            "ttss": 60,
            "ttts": 50,
            "g": 50,
            "gf": 40
        },
        "articulation style": {
            "none": 90,
            "staccato": 60,
            "legato": 50
        }
    }
}