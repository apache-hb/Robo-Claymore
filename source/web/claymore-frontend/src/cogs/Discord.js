import React from 'react'
import logo from '../icons/discord.svg'

export default class Discord extends React.Component {
  render() {
    return (
      <a href="#discord" className="sidebar-item" onClick={() => this.props.onClick(this)}>
        <img src={logo} alt="discord_logo"/>
        Discord
      </a>
    )
  }
}

class DiscordContent extends React.Component {
  render() {
    return <div>CCCC</div>
  }
}

Discord.content = <DiscordContent/>