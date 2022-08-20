import { Filter, ResultsModel } from "../models/resultsModel";
import { get, writable, Writable } from "svelte/store";
import type { Location } from "../models"
import * as L from 'leaflet';

export class MapPresenter {
  rankedList: Writable<Promise<Location[]>> = writable(null);
  map: any;

  constructor() {
    this.resizeMap = this.resizeMap.bind(this);
    this.initMap = this.initMap.bind(this);
    this.rankedList.set(ResultsModel.getInstance().getRankedList(new Filter()));
  }

  createMap(container: any) {
    let m = L.map(container).setView([45.420, 11.895], 13);
    L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
      {
        attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
          &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
        subdomains: 'abcd',
        maxZoom: 18,
      }
    ).addTo(m);

    return m;
  }

  makeIcon() {
    return new L.Icon({
      iconUrl: './src/assets/icon.png',
      iconSize: [40, 40],
      iconAnchor: [20, 30], // [half of iconSize.x, 3/4 of iconSize.y] dependent on image used
      popupAnchor: [0, -30],
      shadowUrl: null
    });
	}

  createMarker(loc: [number, number]) {
		let marker = L.marker(loc, {icon: this.makeIcon()});
		return marker;
	}

  createPopup(name, score) {
    return `<p>${name}</p>
            <p>${score}</p>`;
  }

  initMap(container: any) {
		get(this.rankedList).then(locations => {
        this.map = this.createMap(container); 
        let markerLayers = L.layerGroup();
        
			  locations.forEach(location => {
				  let m = this.createMarker([location.position.lat, location.position.long]);
          m.bindPopup(this.createPopup(location.name, location.score));
          markerLayers.addLayer(m);
			  });

        markerLayers.addTo(this.map);
        
        return {
          destroy: () => { this.map.remove(); this.map=null; }
        };
		})
	}

  resizeMap() {
    if(this.map) this.map.invalidateSize();
  }
}
