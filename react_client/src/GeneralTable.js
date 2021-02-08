import React from 'react'

const GeneralList = ({ data }) => (
  <ul>
    <li>Game count: {data.games}</li>
    <li>Total team kills: {data.kills}</li>
    <li>Total team damage: {data.damage}</li>
  </ul>
)

export default GeneralList