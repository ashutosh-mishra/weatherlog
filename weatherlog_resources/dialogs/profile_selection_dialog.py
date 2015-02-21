# -*- coding: utf-8 -*-


# This file defines the generic dialog for selecting a profile.


# Import GTK for the dialog.
from gi.repository import Gtk


class ProfileSelectionDialog(Gtk.Dialog):
    """Shows the profile selection dialog."""
    def __init__(self, parent, title, profiles, select_mode = "single"):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL)
        self.set_default_size(400, 300)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        sel_box = self.get_content_area()
        sel_grid = Gtk.Grid()
        sel_box.add(sel_grid)
        
        # Create the label.
        sel_lbl = Gtk.Label("Choose dataset:")
        sel_lbl.set_alignment(0, 0.5)
        sel_grid.add(sel_lbl)
        
        # Create the Profile, Creation Date, and Last Modified Date columns.
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model = self.liststore)
        pro_text = Gtk.CellRendererText()
        self.pro_col = Gtk.TreeViewColumn("Dataset", pro_text, text = 0)
        self.treeview.append_column(self.pro_col)
        cre_text = Gtk.CellRendererText()
        self.cre_text = Gtk.TreeViewColumn("Creation Date", cre_text, text = 1)
        self.treeview.append_column(self.cre_text)
        mod_text = Gtk.CellRendererText()
        self.mod_col = Gtk.TreeViewColumn("Last Modified Date", mod_text, text = 2)
        self.treeview.append_column(self.mod_col)
        
        # Allow for multiple items to be selected, if appropriate.
        if select_mode == "multiple":
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        
        # Add the profiles.
        for i in profiles:
            self.liststore.append(i)
        
        # Display the UI.
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_vexpand(True)
        scrolled_win.set_hexpand(True)
        scrolled_win.add(self.treeview)
        sel_grid.attach_next_to(scrolled_win, sel_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
