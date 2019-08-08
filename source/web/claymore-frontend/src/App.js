import React from 'react';
import './App.css';

import Discord from './cogs/Discord'
import GitHub from './cogs/Github'
import Youtube from './cogs/Youtube'
import Artstation from './cogs/Artstation'

// main app thingy
export default class App extends React.Component {
  sidebarClick(comp) {
    this.setState({
      content: comp.content
    })
  }

  render() {
    return (
      <div className="body">
        <div className="sidebar">
          <Discord onClick={this.sidebarClick}/>
          <GitHub onClick={this.sidebarClick}/>
          <Youtube onClick={this.sidebarClick}/>
          <Artstation onClick={this.sidebarClick}/>
        </div>

        <div className="content">

        </div>
      </div>
    )
  }
}
