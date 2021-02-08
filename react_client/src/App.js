import React, { useState } from 'react';
import UsernameForm from "./UsernameForm"
import GeneralTable from "./GeneralTable"
import KillStealTable from "./KillStealTable"
import axios from 'axios'

const App = () => {
	const [request, setRequest] = useState({ state: null })

	const getData = summonerNames => {
		setRequest({ state: "PENDING" })
		axios.post(process.env.REACT_APP_SERVER_URL + 'api/', {
			data: summonerNames
		})
			.then(response => { 
				setRequest({ state: "COMPLETED", response })
			})
			.catch(response => {
				setRequest({ state: "FAILED", response })
			})
	}

  return (
    <div>
      <UsernameForm getData={getData} />
			{request.state === "PENDING" && <p>Loading...</p>}
			{request.state === "FAILED" && <p style={{ color: 'red' }}>{request.response.message}</p>}
			{request.state === "COMPLETED" && <CompletedApp data={request.response.data} />}
    </div>
  );
}

const CompletedApp = ({ data }) => {
	const { ksScoreData, ...generalData } = data

	return (
		<div>
			<GeneralTable data={generalData} />
			<KillStealTable data={ksScoreData} totalData={generalData} />
		</div>
	)
}

export default App;
