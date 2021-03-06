# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk
# Import convert for converting between color systems.
import weatherlog_resources.convert as convert
# Import the application constants.
from weatherlog_resources.constants import *


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Reset", DialogResponse.RESET)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the tab notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        
        # Create the General tab.
        gen_grid = Gtk.Grid()
        gen_grid.set_hexpand(True)
        gen_grid.set_vexpand(True)
        gen_grid.set_column_spacing(10)
        gen_grid.set_row_spacing(5)
        gen_grid_lbl = Gtk.Label("General")
        
        # Create the pre-fill data checkbox.
        self.pre_chk = Gtk.CheckButton("Automatically fill data")
        self.pre_chk.set_tooltip_text("Automatically fill in fields when adding new data. Note that this requires the location to be set as well.")
        self.pre_chk.set_margin_left(5)
        self.pre_chk.set_margin_right(5)
        self.pre_chk.set_margin_top(5)
        self.pre_chk.set_active(config["pre-fill"])
        gen_grid.attach(self.pre_chk, 0, 0, 2, 1)
        
        # Create the confirm deletions checkbox.
        self.del_chk = Gtk.CheckButton("Confirm deletions")
        self.del_chk.set_tooltip_text("Confirm when deleting data or datasets.")
        self.del_chk.set_margin_left(5)
        self.del_chk.set_margin_right(5)
        self.del_chk.set_active(config["confirm_del"])
        gen_grid.attach_next_to(self.del_chk, self.pre_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the import all checkbox.
        self.imp_chk = Gtk.CheckButton("Import all")
        self.imp_chk.set_tooltip_text("Automatically import all data from the file that has been selected to import.")
        self.imp_chk.set_margin_left(5)
        self.imp_chk.set_margin_right(5)
        self.imp_chk.set_active(config["import_all"])
        gen_grid.attach_next_to(self.imp_chk, self.del_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the Location entry.
        loc_lbl = Gtk.Label("Location: ")
        loc_lbl.set_tooltip_text("Location used for automatically filling in fields when adding new data. Note that this must be a 5-digit US zip code.")
        loc_lbl.set_margin_left(5)
        loc_lbl.set_alignment(0, 0.5)
        gen_grid.attach_next_to(loc_lbl, self.imp_chk, Gtk.PositionType.BOTTOM, 1, 1)
        self.loc_ent = Gtk.Entry()
        self.loc_ent.set_margin_right(5)
        self.loc_ent.set_hexpand(True)
        self.loc_ent.set_max_length(5)
        self.loc_ent.connect("changed", self.filter_numbers)
        self.loc_ent.set_text(config["location"])
        gen_grid.attach_next_to(self.loc_ent, loc_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Units combobox.
        unit_lbl = Gtk.Label("Units: ")
        unit_lbl.set_tooltip_text("Measurement units used for display and conversion.")
        unit_lbl.set_margin_left(5)
        unit_lbl.set_alignment(0, 0.5)
        gen_grid.attach_next_to(unit_lbl, loc_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.unit_com = Gtk.ComboBoxText()
        self.unit_com.set_margin_right(5)
        self.unit_com.set_margin_bottom(5)
        self.unit_com.set_hexpand(True)
        for i in ["Metric", "Imperial"]:
            self.unit_com.append_text(i)
        self.unit_com.set_active(["Metric", "Imperial"].index(config["units"].title()))
        gen_grid.attach_next_to(self.unit_com, unit_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Interface tab.
        int_grid = Gtk.Grid()
        int_grid.set_hexpand(True)
        int_grid.set_vexpand(True)
        int_grid.set_column_spacing(10)
        int_grid.set_row_spacing(5)
        int_grid_lbl = Gtk.Label("Interface")
        
        # Create the Restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_tooltip_text("Automatically restore window size on application start to the size when previously closed.")
        self.win_chk.set_margin_left(5)
        self.win_chk.set_margin_right(5)
        self.win_chk.set_margin_top(5)
        self.win_chk.set_active(config["restore"])
        int_grid.add(self.win_chk)
        
        # Create the Show dates in title checkbox.
        self.date_chk = Gtk.CheckButton("Show dates in title")
        self.date_chk.set_tooltip_text("Show starting and ending dates of the dataset in the title bar.")
        self.date_chk.set_margin_left(5)
        self.date_chk.set_margin_right(5)
        self.date_chk.set_active(config["show_dates"])
        int_grid.attach_next_to(self.date_chk, self.win_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the Show units in list checkbox.
        self.unit_chk = Gtk.CheckButton("Show units in list")
        self.unit_chk.set_tooltip_text("Show measurement units in the data list headers.")
        self.unit_chk.set_margin_left(5)
        self.unit_chk.set_margin_right(5)
        self.unit_chk.set_active(config["show_units"])
        int_grid.attach_next_to(self.unit_chk, self.date_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the show pre-fill dialog checkbox.
        self.pdl_chk = Gtk.CheckButton("Show data filling window")
        self.pdl_chk.set_tooltip_text("Show a window when data fields have been automatically filled.")
        self.pdl_chk.set_margin_left(5)
        self.pdl_chk.set_margin_right(5)
        self.pdl_chk.set_active(config["show_pre-fill"])
        int_grid.attach_next_to(self.pdl_chk, self.unit_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the confirm exit checkbox.
        self.cex_chk = Gtk.CheckButton("Confirm application close")
        self.cex_chk.set_tooltip_text("Show a confirmation window when closing the application.")
        self.cex_chk.set_margin_left(5)
        self.cex_chk.set_margin_right(5)
        self.cex_chk.set_active(config["confirm_exit"])
        int_grid.attach_next_to(self.cex_chk, self.pdl_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the truncate notes checkbox.
        self.trun_chk = Gtk.CheckButton("Truncate notes")
        self.trun_chk.set_tooltip_text("Display the Notes field in a truncated form for long entries.")
        self.trun_chk.set_margin_left(5)
        self.trun_chk.set_margin_right(5)
        self.trun_chk.set_margin_bottom(5)
        self.trun_chk.set_active(config["truncate_notes"])
        int_grid.attach_next_to(self.trun_chk, self.cex_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the Graphs tab.
        graph_grid = Gtk.Grid()
        graph_grid.set_hexpand(True)
        graph_grid.set_vexpand(True)
        graph_grid.set_column_spacing(10)
        graph_grid.set_row_spacing(5)
        graph_grid_lbl = Gtk.Label("Graphs")
        
        # Create the graph color selector.
        graph_color_lbl = Gtk.Label("Graph color: ")
        graph_color_lbl.set_tooltip_text("Select the color used for the graphs.")
        graph_color_lbl.set_margin_left(5)
        graph_color_lbl.set_margin_top(5)
        graph_color_lbl.set_alignment(0, 0.5)
        graph_grid.add(graph_color_lbl)
        self.graph_color_btn = Gtk.ColorButton()
        self.graph_color_btn.set_hexpand(True)
        self.graph_color_btn.set_margin_right(5)
        self.graph_color_btn.set_margin_top(5)
        color_rgba = convert.hex_to_rgba(config["graph_color"])
        default_color = Gdk.RGBA(red = color_rgba[0], green = color_rgba[1], blue = color_rgba[2])
        self.graph_color_btn.set_rgba(default_color)
        graph_grid.attach_next_to(self.graph_color_btn, graph_color_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the line width selector.
        width_lbl = Gtk.Label("Line width: ")
        width_lbl.set_tooltip_text("Select the line width.")
        width_lbl.set_margin_left(5)
        width_lbl.set_alignment(0, 0.5)
        graph_grid.attach_next_to(width_lbl, graph_color_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        width_adj = Gtk.Adjustment(lower = 1, upper = 10, step_increment = 1)
        self.width_sbtn = Gtk.SpinButton(digits = 0, adjustment = width_adj)
        self.width_sbtn.set_numeric(False)
        self.width_sbtn.set_margin_right(5)
        self.width_sbtn.set_value(config["line_width"])
        graph_grid.attach_next_to(self.width_sbtn, width_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the line style selector.
        line_lbl = Gtk.Label("Line style: ")
        line_lbl.set_tooltip_text("Select the style used for graph lines.")
        line_lbl.set_margin_left(5)
        line_lbl.set_alignment(0, 0.5)
        graph_grid.attach_next_to(line_lbl, width_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.line_com = Gtk.ComboBoxText()
        self.line_com.set_margin_right(5)
        for i in ["Solid", "Dashes", "Dots", "Dashes and dots"]:
            self.line_com.append_text(i)
        self.line_com.set_active(["Solid", "Dashes", "Dots", "Dashes and dots"].index(config["line_style"])) 
        graph_grid.attach_next_to(self.line_com, line_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the bar chart style selector.
        hatch_styles = ["Solid", "Large upward stripes", "Small upward stripes", "Large downward stripes", "Small downward stripes", \
                        "Horizontal stripes", "Crosshatch", "Diagonal crosshatch", "Stars", "Dots", "Small circles", "Large circles"]
        hatch_lbl = Gtk.Label("Bar chart style: ")
        hatch_lbl.set_tooltip_text("Select the style used for bar charts.")
        hatch_lbl.set_margin_left(5)
        hatch_lbl.set_margin_bottom(5)
        hatch_lbl.set_alignment(0, 0.5)
        graph_grid.attach_next_to(hatch_lbl, line_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.hatch_com = Gtk.ComboBoxText()
        self.hatch_com.set_margin_right(5)
        self.hatch_com.set_margin_bottom(5)
        for i in hatch_styles:
            self.hatch_com.append_text(i)
        self.hatch_com.set_active(hatch_styles.index(config["hatch_style"]))
        graph_grid.attach_next_to(self.hatch_com, hatch_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Technical tab.
        tech_grid = Gtk.Grid()
        tech_grid.set_hexpand(True)
        tech_grid.set_vexpand(True)
        tech_grid.set_column_spacing(10)
        tech_grid.set_row_spacing(5)
        tech_grid_lbl = Gtk.Label("Technical")
        
        # Create the pastebin devkey entry.
        paste_lbl = Gtk.Label("Pastebin API key: ")
        paste_lbl.set_tooltip_text("API key used for uploading to Pastebin.com.\n\nPlease replace with your own if you use this feature frequently.")
        paste_lbl.set_margin_left(5)
        paste_lbl.set_margin_top(5)
        paste_lbl.set_margin_bottom(5) 
        paste_lbl.set_alignment(0, 0.5)
        tech_grid.add(paste_lbl)
        self.paste_ent = Gtk.Entry()
        self.paste_ent.set_margin_right(5)
        self.paste_ent.set_margin_top(5)
        self.paste_ent.set_margin_bottom(5) 
        self.paste_ent.set_hexpand(True)
        self.paste_ent.set_text(config["pastebin"])
        tech_grid.attach_next_to(self.paste_ent, paste_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Display the interface.
        opt_box = self.get_content_area()
        opt_box.add(notebook)
        notebook.append_page(gen_grid, gen_grid_lbl)
        notebook.append_page(int_grid, int_grid_lbl)
        notebook.append_page(graph_grid, graph_grid_lbl)
        notebook.append_page(tech_grid, tech_grid_lbl)
        
        # Connect 'Enter' key to the OK button.
        ok_btn = self.get_widget_for_response(response_id = Gtk.ResponseType.OK)
        ok_btn.set_can_default(True)
        ok_btn.grab_default()
        
        # Show the dialog.
        self.show_all()
    
    
    def filter_numbers(self, event):
        """Filters non-numbers out of the entry."""
        
        text = self.loc_ent.get_text()
        self.loc_ent.set_text("".join([i for i in text if i in "0123456789"]))
