import React from 'react';
import useQueryString from "./useQueryString"

const UsernameForm = ({ getData }) => {

  const [usernameOne, setUsernameOne] = useQueryString("usernameOne", "")
  const [usernameTwo, setUsernameTwo] = useQueryString("usernameTwo", "")
  const [usernameThree, setUsernameThree] = useQueryString("usernameThree", "")
  const [usernameFour, setUsernameFour] = useQueryString("usernameFour", "")
  const [usernameFive, setUsernameFive] = useQueryString("usernameFive", "")

  const handleSubmit = event => {
    event.preventDefault()

    let usernameArray = []
    if (usernameOne) { usernameArray.push(usernameOne) }
    if (usernameTwo) { usernameArray.push(usernameTwo) }
    if (usernameThree) { usernameArray.push(usernameThree) }
    if (usernameFour) { usernameArray.push(usernameFour) }
    if (usernameFive) { usernameArray.push(usernameFive) }
    
    getData(usernameArray)
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="usernameOne">Username 1: </label>
        <input 
          id="usernameOne" 
          value={usernameOne} 
          onChange={event => setUsernameOne(event.target.value)} 
        />
      </div>
      <div>
        <label htmlFor="usernameTwo">Username 2: </label>
        <input 
          id="usernameTwo" 
          value={usernameTwo} 
          onChange={event => setUsernameTwo(event.target.value)} 
        />
      </div>
      <div>
        <label htmlFor="usernameThree">Username 3: </label>
        <input 
          id="usernameThree" 
          value={usernameThree} 
          onChange={event => setUsernameThree(event.target.value)} 
        />
      </div>
      <div>
        <label htmlFor="usernameFour">Username 4: </label>
        <input 
          id="usernameFour" 
          value={usernameFour} 
          onChange={event => setUsernameFour(event.target.value)} 
        />
      </div>
      <div>
        <label htmlFor="usernameFive">Username 5: </label>
        <input 
          id="usernameFive" 
          value={usernameFive} 
          onChange={event => setUsernameFive(event.target.value)} 
        />
      </div>
      <button>Go</button>
    </form>
  );
}

export default UsernameForm;
