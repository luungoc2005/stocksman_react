import React from 'react';

import toast from '../css/toast.css'; // Grids

import AppBar from 'material-ui/AppBar';

class Navbar extends React.Component {
  render() {
    return (
        <AppBar
            className={toast.grid}
            title="Material Theme Boilerplate"
            iconElementRight=
            {
              <IconButton>
                <ActionHelp />
              </IconButton>
            }
        >
        </AppBar>
    );
  }
}

export default Navbar;