import React, {Component} from "react";
import logo from "./logo.svg";
import "./App.css";
import "../node_modules/@blueprintjs/core/dist/blueprint.css"
import "../node_modules/normalize.css/normalize.css"
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts";
import { Intent, Spinner, DatePickerFactory, Tab, Tabs, TabList, TabPanel } from "@blueprintjs/core";
const data = [
  {name: 'Page A', uv: 4000, pv: 2400, amt: 2400},
  {name: 'Page B', uv: 3000, pv: 1398, amt: 2210},
  {name: 'Page C', uv: 2000, pv: 9800, amt: 2290},
  {name: 'Page D', uv: 2780, pv: 3908, amt: 2000},
  {name: 'Page E', uv: 1890, pv: 4800, amt: 2181},
  {name: 'Page F', uv: 2390, pv: 3800, amt: 2500},
  {name: 'Page G', uv: 3490, pv: 4300, amt: 2100},
];

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loading: true
    }
  }

  getData() {
    //Grab the data, then will successful promise returned/
    this.setState({loading: false});
  }
  componentDidMount() {

    //Faking data retrieval
    setTimeout(() => {
      this.getData();
    }, 2000);

  }
  render() {

    if (this.state.loading) {
      return (
          <div className="App" style={{marginTop: 50}}>
            <Spinner intent={Intent.PRIMARY} />
          </div>
      )
    }
    return (
        <div className="App">
          <div className="pt-callout .pt-intent-primary">
            <h5>Under Construction</h5>
            Internet of Things Module Dashboard Demo
          </div>

          <nav className="pt-navbar .modifier">
            <div className="pt-navbar-group pt-align-left">
              <div className="pt-navbar-heading">Blueprint</div>
              <input className="pt-input" placeholder="Search files..." type="text" />
            </div>
            <div className="pt-navbar-group pt-align-right">
              <button className="pt-button pt-minimal pt-icon-home">Home</button>
              <button className="pt-button pt-minimal pt-icon-document">Files</button>
              <span className="npmpt-navbar-divider"></span>
              <button className="pt-button pt-minimal pt-icon-user"></button>
              <button className="pt-button pt-minimal pt-icon-notifications"></button>
              <button className="pt-button pt-minimal pt-icon-cog"></button>
            </div>
          </nav>

          <div className="App-header">
            <img src={logo} className="App-logo" alt="logo"/>
          </div>
          <Tabs>
            <TabList>
              <Tab>First tab</Tab>
              <Tab>Second tab</Tab>
              <Tab>Third tab</Tab>
              <Tab isDisabled={true}>Fourth tab</Tab>
            </TabList>
            <TabPanel>
              First panel
            </TabPanel>
            <TabPanel>
              Second panel
            </TabPanel>
            <TabPanel>
              Third panel
            </TabPanel>
            <TabPanel>
              Fourth panel
            </TabPanel>
          </Tabs>

          <LineChart width={600} height={300} data={data}
                     margin={{top: 5, right: 30, left: 20, bottom: 5}}>
            <XAxis dataKey="name"/>
            <YAxis/>
            <CartesianGrid strokeDasharray="3 3"/>
            <Tooltip/>
            <Legend />
            <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{r: 8}}/>
            <Line type="monotone" dataKey="uv" stroke="#82ca9d"/>
          </LineChart>
        </div>
    );
  }
}

export default App;
