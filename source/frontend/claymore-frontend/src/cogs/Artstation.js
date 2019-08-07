import React from 'react'
import logo from '../icons/artstation.svg'

export default class Discord extends React.Component {
  render() {
    return (
      <a href="#artstation" className="sidebar-item">
        <img src={logo} alt="logo"/>
        Artstation
      </a>
    )
  }
}