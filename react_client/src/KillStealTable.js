import React from 'react'

const KillStealTable = ({ data, totalData }) => (
  <table>
    <thead>
      <tr>
        <td>
          <strong>Summoner name</strong>
        </td>
        <td>
          <strong>KS score</strong>
        </td>
        <td>
          <strong>Kills</strong>
        </td>
        <td>
          <strong>Total kills</strong>
        </td>
        <td>
          <strong>Kill %</strong>
        </td>
        <td>
          <strong>Damage</strong>
        </td>
        <td>
          <strong>Total damage</strong>
        </td>
        <td>
          <strong>Damage %</strong>
        </td>
      </tr>
    </thead>

    <tbody>
      {data.map(summoner => 
        <tr key={summoner.summonerName}>
          <td>
            <strong>{summoner.summonerName}</strong>
          </td>
          <td>
            <strong>{summoner.ksScore}</strong>
          </td>
          <td>{summoner.kills}</td>
          <td>{totalData.kills}</td>
          <td>{summoner.killPercentage}</td>
          <td>{summoner.damage}</td>
          <td>{totalData.damage}</td>
          <td>{summoner.damagePercentage}</td>
        </tr>
      )}
    </tbody>
  </table>
)

export default KillStealTable