# -*- coding: utf-8 -*-

import nuke

import nomenclator

menu_bar = nuke.menu("Nuke")
menu = menu_bar.addMenu("&File")
menu.addCommand("Nomenclator - Manage Comp...", nomenclator.open_comp_manager_dialog, index=0)
menu.addCommand("Nomenclator - Manage Outputs...", nomenclator.open_output_manager_dialog, index=1)
menu.addCommand("Nomenclator - Settings...", nomenclator.open_settings_dialog, index=2)
menu.addSeparator(index=3)
