import React from 'react'
import logo from '../icons/youtube.svg'

export default class Youtube extends React.Component {
  render() {
    return (
      <a href="#youtube" className="sidebar-item" onClick={() => this.props.onClick(this)}>
        <img src={logo} alt="youtube_logo"/>
        Youtube
      </a>
    )
  }
}

class YoutubeContent extends React.Component {
  render() {
    return <div>BBBBB</div>
  }
}

Youtube.content = <YoutubeContent/>