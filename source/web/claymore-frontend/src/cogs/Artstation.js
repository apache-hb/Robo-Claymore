import React from 'react'
import logo from '../icons/artstation.svg'

export default class Artstation extends React.Component {
  render() {
    return (
      <a href="#artstation" className="sidebar-item" onClick={() => this.props.onClick(this)}>
        <img src={logo} alt="logo"/>
        Artstation
      </a>
    )
  }
}

class ArtstationContent extends React.Component {
  render() {
    return <div>DDDDD</div>
  }
}

Artstation.content = <ArtstationContent/>