import * as React from "react";
import { Admin, Resource, ListGuesser } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";
import authProvider from "./authProvider";
import { AccountList } from "./accounts";
const dataProvider = simpleRestProvider("http://localhost:8082"); // account-service
function App() {
  return (
    <Admin
      dataProvider={dataProvider}
      authProvider={authProvider}
      title="Banking Dashboard"
    >
      <Resource name="accounts" list={AccountList} />
    </Admin>
  );
}
export default App;
