import React from 'react'
import logo from '../icons/youtube.svg'

export default class Youtube extends React.Component {
  render() {
    return (
      <a href="#youtube" className="sidebar-item">
        <img src={logo} alt="youtube_logo"/>
        Youtube
      </a>
    )
  }
}