import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
// @material-ui/icons
import Camera from "@material-ui/icons/Camera";
import Palette from "@material-ui/icons/Palette";
import Favorite from "@material-ui/icons/Favorite";
// core components
import Header from "components/Header/Header.jsx";
import Footer from "components/Footer/Footer.jsx";
import Button from "components/CustomButtons/Button.jsx";
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import HeaderLinks from "components/Header/HeaderLinks.jsx";
import NavPills from "components/NavPills/NavPills.jsx";
import Parallax from "components/Parallax/Parallax.jsx";

import profile from "assets/img/faces/christian.jpg";

import studio1 from "assets/img/examples/studio-1.jpg";
import studio2 from "assets/img/examples/studio-2.jpg";
import studio3 from "assets/img/examples/studio-3.jpg";
import studio4 from "assets/img/examples/studio-4.jpg";
import studio5 from "assets/img/examples/studio-5.jpg";
import work1 from "assets/img/examples/olu-eletu.jpg";
import work2 from "assets/img/examples/clem-onojeghuo.jpg";
import work3 from "assets/img/examples/cynthia-del-rio.jpg";
import work4 from "assets/img/examples/mariya-georgieva.jpg";
import work5 from "assets/img/examples/clem-onojegaw.jpg";

import componentsStyle from "assets/jss/material-kit-react/views/components.jsx";

class Components extends React.Component {
  render() {
    const { classes, ...rest } = this.props;
    return (
      <div>
        <Header
          brand="Statify"
          rightLinks={<HeaderLinks />}
          fixed
          color="transparent"
          changeColorOnScroll={{
            height: 400,
            color: "white"
          }}
          {...rest}
        />

        <Parallax image={require("assets/img/Audio-Waveforms-Featued-Image.jpg")}>
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem>
                <div className={classes.brand}>
                  <h1 className={classes.title}> </h1>
                  <h3 className={classes.subtitle}>
                    To Begin, Select a Genre!
                  </h3>
                </div>
              </GridItem>
            </GridContainer>
              <GridItem xs={12} sm={12} md={8} justify="left">
                <Button href="http://localhost:5000/login?genre=Hip-Hop" color="primary" round>
                  Hip-Hop
                </Button>
                <Button href="http://localhost:5000/login?genre=Rap" color="primary" round>
                  Rap
                  </Button>
                <Button href="http://localhost:5000/login?genre=Pop" color="primary" round>
                  Pop
                  </Button>
                <Button href="http://localhost:5000/login?genre=Rock" color="primary" round>
                  Rock
                  </Button>
                <Button href="http://localhost:5000/login?genre=Classical" color="primary" round>
                  Classical
                  </Button>
                <Button href="http://localhost:5000/login?genre=EDM" color="primary" round>
                  EDM  
                  </Button>
                <Button href="http://localhost:5000/login?genre=Jazz" color="primary" round>
                    Jazz
                  </Button>
                <Button href="http://localhost:5000/login?genre=Latin" color="primary" round>
                    Latin
                  </Button>
                <Button href="http://localhost:5000/login?genre=Indie" color="primary" round>
                    Indie
                  </Button>
                <Button href="http://localhost:5000/login?genre=K-Pop" color="primary" round>
                    K-Pop
                  </Button>
                <Button href="http://localhost:5000/login?genre=Reggae" color="primary" round>
                  Reggae
                  </Button>
                <Button href="http://localhost:5000/login?genre=Worship" color="primary" round>
                    Worship
                  </Button>
                <Button href="http://localhost:5000/login?genre=Sleep" color="primary" round>
                    Sleep
                  </Button>
              </GridItem>
          </div>
        </Parallax>

        
        <Footer />
      </div>
    );
  }
}

export default withStyles(componentsStyle)(Components);
