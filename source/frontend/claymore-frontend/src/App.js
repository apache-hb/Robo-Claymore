import React from 'react';
import './App.css';

import Discord from './cogs/Discord'
import GitHub from './cogs/Github'
import Youtube from './cogs/Youtube'
import Artstation from './cogs/Artstation'

let cogs = [
  GitHub,
  Discord,
  Youtube,
  Artstation
]

// main app thingy
export default class App extends React.Component {
  render() {
    return (
      <div className="body">
        <div className="sidebar">
          {cogs.map(cog => React.createElement(cog, { key: cog.name }))}
        </div>

        <div className="content">
          {GitHub.content}
        </div>
      </div>
    )
  }
}
