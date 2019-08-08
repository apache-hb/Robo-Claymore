import React from 'react'
import logo from '../icons/github.svg'

export default class GitHub extends React.Component {
  render() {
    return (
      <a href="#github" className="sidebar-item" onClick={() => this.props.onClick(this)}>
        <img src={logo} alt="github_logo"/>
        GitHub
      </a>
    )
  }
}

class GitHubContent extends React.Component {
  render() {
    return <div>AAAA</div>
  }
}

GitHub.content = <GitHubContent/>