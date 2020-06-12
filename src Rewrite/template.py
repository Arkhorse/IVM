import Keys

class Template(object):

    def __init__(self):
        self.defaultKeys = {
            'buttonRepair' : [Keys.KEY_SPACE],
            'buttonChassis': [[Keys.KEY_LALT, Keys.KEY_RALT]]
        }
        self.config = {'templates': {
                'modDisplayName': 'Improved Visuals and Sounds',
                'settingsVersion': 0.2,
                'enabled': True,
                'column1': [
                    {
                        'type': 'Label',
                        'text': 'In Battle Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Missions Hint UI',
                        'value': False,
                        'tooltip': '{BODY} Turn this off if you dont want the missions hint UI at the start of the battle {/ BODY}',
                        'varName': 'questHintEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'Sound Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Stun Sound',
                        'value': False,
                        'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are stunned. {/ HEADER} {BODY} This is the DeadPool one {/ BODY}',
                        'varName': 'stunEnabled'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Fire Sound',
                        'value': False,
                        'tooltip': '{HEADER} Turn this on if you want a Voice Over for when you are set on fire. {/ HEADER} {BODY} This is the DeadPool one. {/ BODY}',
                        'varName': 'fireEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'In Garage Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Carousel Function',
                        'value': False,
                        'tooltip': '{BODY} Turn this on if you want to use the carousel stuff{/ BODY}',
                        'varName': 'carEnabled'
                    },
                    {
                        'type': 'Slider',
                        'text': 'The number of carousel rows you want',
                        'minimum': 1,
                        'maximum': 12,
                        'snapInterval': 1,
                        'value': 1,
                        'format': '{{value}}',
                        'varName': 'carRows'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable Garage Counters',
                        'value': True,
                        'varName': 'counterEnabled'
                    },
                    {
                        'type': 'Label',
                        'text': 'Fixes, Ect'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Effects List Spam',
                        'tooltip': 'Removes the effects list spam from the python.log. This can cause this log to be very large. #WG',
                        'value': False,
                        'varName': 'fixEffects'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Vehicle Model Transparency',
                        'tooltip': 'Fixes a rare issue where the vehicle model isnt shown correctly',
                        'value': False,
                        'varName': 'fixVehicleTransparency'
                    },
                ],
                'column2': [
                    {
                        'type': 'Label',
                        'text': 'Repair Options'
                    },
                    {
                        'type': 'Label',
                        'text': 'Repair Options is legal. None of these options are automatic.'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Enable',
                        'value': False,
                        'varName': 'repairEnabled'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Repair Tracks and Wheels',
                        'value': [Keys.KEY_SPACE],
                        'varName': 'buttonChassis'
                    },
                    {
                        'type': 'HotKey',
                        'text': 'Smart Repair',
                        'value': [[Keys.KEY_LALT, Keys.KEY_RALT]],
                        'varName': 'buttonRepair'
                    },
                    {
                        'type': 'Label',
                        'text': 'Smart Repair Options'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Use Gold Kits',
                        'value': False,
                        'varName': 'useGoldKits'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair Tracks and Wheels',
                        'value': False,
                        'varName': 'restoreChassis'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Repair all Devices (Optics, Turret, Gun, Ect)',
                        'value': False,
                        'varName': 'repairDevices'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Heal Crew',
                        'value': False,
                        'varName': 'healCrew'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Extinguish Fires',
                        'value': False,
                        'varName': 'extinguishFire'
                    },
                    {
                        'type': 'CheckBox',
                        'text': 'Remove Stun',
                        'value': False,
                        'varName': 'removeStun'
                    }]
                }, 'settings': {
                'enabled': True,
                'carEnabled': False,
                'carRows': 1,
                'questHintEnabled': True,
                'counterEnabled': True,
                'stunEnabled': False,
                'stunEvent': 'battle_event_stun',
                'fireEnabled': False,
                'fireEvent': 'battle_event_fire',
                'fixEffects': False,
                'fixVehicleTransparency': False,
                'emptyShellsEnabled': False,
                'emptyShellsEvent': 'IVM_emptyShellsEvent',
                'almostOutEvent': 'IVM_almostOutEvent',
                'TESTER': True,
                'repairEnabled': False,
                'buttonChassis' : self.defaultKeys['buttonChassis'],
                'buttonRepair'  : self.defaultKeys['buttonRepair'],
                'removeStun'    : True,
                'extinguishFire': True,
                'healCrew': True,
                'repairDevices': True,
                'restoreChassis': True,
                'useGoldKits'   : False,
                'repairPriority': {
                    'lightTank'            : {
                        'medkit'   : ['commander', 'driver', 'gunner', 'loader'],
                        'repairkit': ['ammoBay', 'engine', 'gun', 'turretRotator', 'fuelTank']
                    },
                    'mediumTank'           : {
                        'medkit'   : ['commander', 'loader', 'driver', 'gunner'],
                        'repairkit': ['ammoBay', 'turretRotator', 'engine', 'gun', 'fuelTank']
                    },
                    'heavyTank'            : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'turretRotator', 'engine', 'fuelTank']
                    },
                    'SPG'                  : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AT-SPG'               : {
                        'medkit'   : ['commander', 'loader', 'gunner', 'driver'],
                        'repairkit': ['ammoBay', 'gun', 'engine', 'turretRotator', 'fuelTank']
                    },
                    'AllAvailableVariables': {
                        'medkit'   : ['commander', 'gunner', 'driver', 'radioman', 'loader'],
                        'repairkit': ['engine', 'ammoBay', 'gun', 'turretRotator', 'chassis', 'surveyingDevice', 'radio', 'fuelTank', 'wheel']
                    }
                }
            }}
