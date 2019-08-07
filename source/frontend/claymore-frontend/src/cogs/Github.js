import React from 'react'
import logo from '../icons/github.svg'

export default class GitHub extends React.Component {
  render() {
    return (
      <a href="#github" className="sidebar-item">
        <img src={logo} alt="github_logo"/>
        GitHub
      </a>
    )
  }
}

class GitHubContent extends React.Component {
  render() {
    return <div></div>
  }
}

GitHub.content = <GitHubContent/>