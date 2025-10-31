import * as React from "react";
import { List, Datagrid, TextField, NumberField } from "react-admin";
export const AccountList = (props) => (
  <List {...props} title="Comptes bancaires">
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" label="Client" />
      <NumberField source="balance" label="Solde (€)" />
    </Datagrid>
  </List>
);
