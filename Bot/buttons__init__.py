from button import BUTTONS_SETTINGS as bs

Accept = bs.get('accept')
Deny = bs.get('deny')
Rock, Paper, Sciss = bs['rock'], bs['paper'], bs['scissors']
Sniper, Solder, Demoman = bs['sniper'], bs['solder'], bs['demoman']
Body_Sh, Head_Sh, Move_R, Move_L = bs['body_shot'], bs['head_shot'], bs['move_R'], bs['move_L']
Units = bs['units']
menu_set = bs['menu_setting']
Stat = menu_set['stat']
Back = bs['back']
Sniper_up = menu_set['units']['sniper']
Solder_up = menu_set['units']['solder']
Demoman_up = menu_set['units']['demoman']
Damage, Health, Accuracy = menu_set['lvl_up']['damage'], menu_set['lvl_up']['health'], menu_set['lvl_up']['accuracy']

Sniper_stat, Solder_stat, Demoman_stat = bs['sniper_stat'], bs['solder_stat'], bs['demoman_stat']