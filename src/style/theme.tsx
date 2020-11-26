import {createMuiTheme } from "@material-ui/core/styles";

export const MyTheme = createMuiTheme({
    palette: {
        background: {
          default: "#292929",
        },
        text:{
          primary: "#B12025",
          secondary : "#FFFFFF"
        },
        primary: {
          main:"#B12025",
        },
        secondary : { 
          main: "#E61E25",
        }
    }, 
    overrides: {
      MuiInput : {
        root: {
          color:'#FFF'
        }
      },
      MuiOutlinedInput: {
        root: {
          "& $notchedOutline : ": {
            borderColor: "#FFF"
          },
          "&:hover:not($focused):not($error) $notchedOutline": {
            borderColor: '#FFF',
          },
          "&$focused $notchedOutline": {
            borderColor: "#FFF",
            borderWidth: 1
          },
          color:'#FFF'
        },
       
      },
      MuiFormLabel: {
        root: {
          "&$focused": {
            color: '#FFF'
          },
          color : '#FFF'
        },
      },
      MuiDrawer :{
        paper:{
          backgroundColor :'#292929',
        },
      },
      MuiSelect: {
        
      }
    } 
  });