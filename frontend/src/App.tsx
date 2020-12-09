import React , {useState , useMemo} from 'react';
import {BrowserRouter, Route , Switch} from 'react-router-dom';
import { MuiThemeProvider} from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import {UserContext , UserInterface} from './Context/UserContext';

import Login from './Pages/Login';
import NewScan from './Pages/NewScan'; 
import ViewScans from './Pages/ViewScans';
import Scan from './Pages/Scan';
import ViewTeams from './Pages/ViewTeams';
import Profile from './Pages/Profile';
import Team from './Pages/Team';

import {MyTheme} from './style/theme';

const App = () => {
  const [User, setUser] = useState<UserInterface>({
    'access_token' : "", 
    'surname' : "", 
    'name' : "",
    'mail' : "", 
    'job' : "", 
    'ipMsfrpcd' : ""
  })

  const providerValue = useMemo(() => ({User , setUser}), [User, setUser]);

  return (
    <MuiThemeProvider theme={MyTheme}>
      <CssBaseline />
      <BrowserRouter>
        <Switch> 
          <UserContext.Provider value={providerValue}>
            <Route exact path='/' component={Login}/> 
            <Route exact path='/newScan' component={NewScan}/> 
            <Route exact path='/scans' component={ViewScans}/> 
            <Route exact path='/scan/:id' component={Scan}/> 
            <Route exact path='/teams' component={ViewTeams}/>
            <Route exact path='/team/:id' component={Team}/>
            <Route exact path='/profile' component={Profile}/>
          </UserContext.Provider> 
        </Switch>
    </BrowserRouter>
    </MuiThemeProvider> 
    
  )
}

export default App
