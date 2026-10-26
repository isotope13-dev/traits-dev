"""GPU inference worker: registers its public address with the pool."""
import base64, io, logging, requests

MODEL_ID = "example/model-1"


def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        return None


async def send_heartbeat(public_ip):
    register_url = "https://pool.example.com/register"
    async with aiohttp.ClientSession() as session:
        async with session.post(register_url, json={"url": f"http://{public_ip}:8766"}) as resp:
            logging.info("heartbeat %s", resp.status)

# worker tuning note 0: batch size, queue depth, retry budget
RATE_0 = 0
# worker tuning note 1: batch size, queue depth, retry budget
RATE_1 = 1
# worker tuning note 2: batch size, queue depth, retry budget
RATE_2 = 2
# worker tuning note 3: batch size, queue depth, retry budget
RATE_3 = 3
# worker tuning note 4: batch size, queue depth, retry budget
RATE_4 = 4
# worker tuning note 5: batch size, queue depth, retry budget
RATE_5 = 5
# worker tuning note 6: batch size, queue depth, retry budget
RATE_6 = 6
# worker tuning note 7: batch size, queue depth, retry budget
RATE_7 = 7
# worker tuning note 8: batch size, queue depth, retry budget
RATE_8 = 8
# worker tuning note 9: batch size, queue depth, retry budget
RATE_9 = 9
# worker tuning note 10: batch size, queue depth, retry budget
RATE_10 = 10
# worker tuning note 11: batch size, queue depth, retry budget
RATE_11 = 11
# worker tuning note 12: batch size, queue depth, retry budget
RATE_12 = 12
# worker tuning note 13: batch size, queue depth, retry budget
RATE_13 = 13
# worker tuning note 14: batch size, queue depth, retry budget
RATE_14 = 14
# worker tuning note 15: batch size, queue depth, retry budget
RATE_15 = 15
# worker tuning note 16: batch size, queue depth, retry budget
RATE_16 = 16
# worker tuning note 17: batch size, queue depth, retry budget
RATE_17 = 17
# worker tuning note 18: batch size, queue depth, retry budget
RATE_18 = 18
# worker tuning note 19: batch size, queue depth, retry budget
RATE_19 = 19
# worker tuning note 20: batch size, queue depth, retry budget
RATE_20 = 20
# worker tuning note 21: batch size, queue depth, retry budget
RATE_21 = 21
# worker tuning note 22: batch size, queue depth, retry budget
RATE_22 = 22
# worker tuning note 23: batch size, queue depth, retry budget
RATE_23 = 23
# worker tuning note 24: batch size, queue depth, retry budget
RATE_24 = 24
# worker tuning note 25: batch size, queue depth, retry budget
RATE_25 = 25
# worker tuning note 26: batch size, queue depth, retry budget
RATE_26 = 26
# worker tuning note 27: batch size, queue depth, retry budget
RATE_27 = 27
# worker tuning note 28: batch size, queue depth, retry budget
RATE_28 = 28
# worker tuning note 29: batch size, queue depth, retry budget
RATE_29 = 29
# worker tuning note 30: batch size, queue depth, retry budget
RATE_30 = 30
# worker tuning note 31: batch size, queue depth, retry budget
RATE_31 = 31
# worker tuning note 32: batch size, queue depth, retry budget
RATE_32 = 32
# worker tuning note 33: batch size, queue depth, retry budget
RATE_33 = 33
# worker tuning note 34: batch size, queue depth, retry budget
RATE_34 = 34
# worker tuning note 35: batch size, queue depth, retry budget
RATE_35 = 35
# worker tuning note 36: batch size, queue depth, retry budget
RATE_36 = 36
# worker tuning note 37: batch size, queue depth, retry budget
RATE_37 = 37
# worker tuning note 38: batch size, queue depth, retry budget
RATE_38 = 38
# worker tuning note 39: batch size, queue depth, retry budget
RATE_39 = 39
# worker tuning note 40: batch size, queue depth, retry budget
RATE_40 = 40
# worker tuning note 41: batch size, queue depth, retry budget
RATE_41 = 41
# worker tuning note 42: batch size, queue depth, retry budget
RATE_42 = 42
# worker tuning note 43: batch size, queue depth, retry budget
RATE_43 = 43
# worker tuning note 44: batch size, queue depth, retry budget
RATE_44 = 44
# worker tuning note 45: batch size, queue depth, retry budget
RATE_45 = 45
# worker tuning note 46: batch size, queue depth, retry budget
RATE_46 = 46
# worker tuning note 47: batch size, queue depth, retry budget
RATE_47 = 47
# worker tuning note 48: batch size, queue depth, retry budget
RATE_48 = 48
# worker tuning note 49: batch size, queue depth, retry budget
RATE_49 = 49
# worker tuning note 50: batch size, queue depth, retry budget
RATE_50 = 50
# worker tuning note 51: batch size, queue depth, retry budget
RATE_51 = 51
# worker tuning note 52: batch size, queue depth, retry budget
RATE_52 = 52
# worker tuning note 53: batch size, queue depth, retry budget
RATE_53 = 53
# worker tuning note 54: batch size, queue depth, retry budget
RATE_54 = 54
# worker tuning note 55: batch size, queue depth, retry budget
RATE_55 = 55
# worker tuning note 56: batch size, queue depth, retry budget
RATE_56 = 56
# worker tuning note 57: batch size, queue depth, retry budget
RATE_57 = 57
# worker tuning note 58: batch size, queue depth, retry budget
RATE_58 = 58
# worker tuning note 59: batch size, queue depth, retry budget
RATE_59 = 59
# worker tuning note 60: batch size, queue depth, retry budget
RATE_60 = 60
# worker tuning note 61: batch size, queue depth, retry budget
RATE_61 = 61
# worker tuning note 62: batch size, queue depth, retry budget
RATE_62 = 62
# worker tuning note 63: batch size, queue depth, retry budget
RATE_63 = 63
# worker tuning note 64: batch size, queue depth, retry budget
RATE_64 = 64
# worker tuning note 65: batch size, queue depth, retry budget
RATE_65 = 65
# worker tuning note 66: batch size, queue depth, retry budget
RATE_66 = 66
# worker tuning note 67: batch size, queue depth, retry budget
RATE_67 = 67
# worker tuning note 68: batch size, queue depth, retry budget
RATE_68 = 68
# worker tuning note 69: batch size, queue depth, retry budget
RATE_69 = 69
# worker tuning note 70: batch size, queue depth, retry budget
RATE_70 = 70
# worker tuning note 71: batch size, queue depth, retry budget
RATE_71 = 71
# worker tuning note 72: batch size, queue depth, retry budget
RATE_72 = 72
# worker tuning note 73: batch size, queue depth, retry budget
RATE_73 = 73
# worker tuning note 74: batch size, queue depth, retry budget
RATE_74 = 74
# worker tuning note 75: batch size, queue depth, retry budget
RATE_75 = 75
# worker tuning note 76: batch size, queue depth, retry budget
RATE_76 = 76
# worker tuning note 77: batch size, queue depth, retry budget
RATE_77 = 77
# worker tuning note 78: batch size, queue depth, retry budget
RATE_78 = 78
# worker tuning note 79: batch size, queue depth, retry budget
RATE_79 = 79
# worker tuning note 80: batch size, queue depth, retry budget
RATE_80 = 80
# worker tuning note 81: batch size, queue depth, retry budget
RATE_81 = 81
# worker tuning note 82: batch size, queue depth, retry budget
RATE_82 = 82
# worker tuning note 83: batch size, queue depth, retry budget
RATE_83 = 83
# worker tuning note 84: batch size, queue depth, retry budget
RATE_84 = 84
# worker tuning note 85: batch size, queue depth, retry budget
RATE_85 = 85
# worker tuning note 86: batch size, queue depth, retry budget
RATE_86 = 86
# worker tuning note 87: batch size, queue depth, retry budget
RATE_87 = 87
# worker tuning note 88: batch size, queue depth, retry budget
RATE_88 = 88
# worker tuning note 89: batch size, queue depth, retry budget
RATE_89 = 89
# worker tuning note 90: batch size, queue depth, retry budget
RATE_90 = 90
# worker tuning note 91: batch size, queue depth, retry budget
RATE_91 = 91
# worker tuning note 92: batch size, queue depth, retry budget
RATE_92 = 92
# worker tuning note 93: batch size, queue depth, retry budget
RATE_93 = 93
# worker tuning note 94: batch size, queue depth, retry budget
RATE_94 = 94
# worker tuning note 95: batch size, queue depth, retry budget
RATE_95 = 95
# worker tuning note 96: batch size, queue depth, retry budget
RATE_96 = 96
# worker tuning note 97: batch size, queue depth, retry budget
RATE_97 = 97
# worker tuning note 98: batch size, queue depth, retry budget
RATE_98 = 98
# worker tuning note 99: batch size, queue depth, retry budget
RATE_99 = 99
# worker tuning note 100: batch size, queue depth, retry budget
RATE_100 = 100
# worker tuning note 101: batch size, queue depth, retry budget
RATE_101 = 101
# worker tuning note 102: batch size, queue depth, retry budget
RATE_102 = 102
# worker tuning note 103: batch size, queue depth, retry budget
RATE_103 = 103
# worker tuning note 104: batch size, queue depth, retry budget
RATE_104 = 104
# worker tuning note 105: batch size, queue depth, retry budget
RATE_105 = 105
# worker tuning note 106: batch size, queue depth, retry budget
RATE_106 = 106
# worker tuning note 107: batch size, queue depth, retry budget
RATE_107 = 107
# worker tuning note 108: batch size, queue depth, retry budget
RATE_108 = 108
# worker tuning note 109: batch size, queue depth, retry budget
RATE_109 = 109
# worker tuning note 110: batch size, queue depth, retry budget
RATE_110 = 110
# worker tuning note 111: batch size, queue depth, retry budget
RATE_111 = 111
# worker tuning note 112: batch size, queue depth, retry budget
RATE_112 = 112
# worker tuning note 113: batch size, queue depth, retry budget
RATE_113 = 113
# worker tuning note 114: batch size, queue depth, retry budget
RATE_114 = 114
# worker tuning note 115: batch size, queue depth, retry budget
RATE_115 = 115
# worker tuning note 116: batch size, queue depth, retry budget
RATE_116 = 116
# worker tuning note 117: batch size, queue depth, retry budget
RATE_117 = 117
# worker tuning note 118: batch size, queue depth, retry budget
RATE_118 = 118
# worker tuning note 119: batch size, queue depth, retry budget
RATE_119 = 119


def encode_image(image):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()
