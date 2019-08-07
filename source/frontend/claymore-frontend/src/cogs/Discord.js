import React from 'react'
import logo from '../icons/discord.svg'

export default class Discord extends React.Component {
  render() {
    return (
      <a href="#discord" className="sidebar-item">
        <img src={logo} alt="discord_logo"/>
        Discord
      </a>
    )
  }
}