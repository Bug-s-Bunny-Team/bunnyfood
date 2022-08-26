import { ResultsModel } from "../models/resultsModel";
import { get, writable, Writable } from "svelte/store";
import { Filter, Location, Position, RequestError } from "../models"
import { capitalizeFirstLetter, error_duration, removeChildren } from "../utils";
import ErrorSvelte from "../components/Error.svelte";
import * as L from 'leaflet';

export class MapPresenter {
  rankedList: Writable<Promise<Location[]>> = writable(null);
  map: any;
  markerLayers: any;
  errorTimeout: NodeJS.Timeout = null;

  lastRefreshPosition: Position = null;
  lastRefreshZoom: number = null;
  treshold_a: number = 100000.0;
  treshold_b: number = 6.2;

  defaultPosition: Position = new Position(45.420, 11.895);
  defaultZoom: number = 13;

  constructor() {
    this.resizeMap = this.resizeMap.bind(this);
    this.initMap = this.initMap.bind(this);
    this.destroy = this.destroy.bind(this);
    this.refresh = this.refresh.bind(this);
    this.createAllMarkers = this.createAllMarkers.bind(this);
    this.createMarker = this.createMarker.bind(this);
  }

  createMap(container: any) {
    let map = L.map(container).setView([this.defaultPosition.lat, this.defaultPosition.long], this.defaultZoom);
    L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
      {
        attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
          &copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
        subdomains: 'abcd',
        minZoom: 4,
        maxZoom: 18,
      }
    ).addTo(map);

    return map;
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

  createPopup(location: Location) {
    return `<p><a href="./home?details_placeid=${location.id}">${capitalizeFirstLetter(location.name)}</a></p>
            <p>${Math.round(location.score*10.0)/10.0}/5</p>`;
  }

  initMap(container: any) {
    this.map = this.createMap(container); 
    this.markerLayers = L.layerGroup();
    this.markerLayers.addTo(this.map);
    this.refresh();
    this.rankedList.subscribe(this.createAllMarkers);
    this.map.on("moveend", this.refresh);
    return {
      destroy: () => { this.map.remove(); this.map=null; }
    };
	}

  createAllMarkers(rankedList: Promise<Location[]>) {
      rankedList.then(locations => {
        this.markerLayers.clearLayers();
        locations.forEach(location => {
          let marker = this.createMarker([location.position.lat, location.position.long]);
          marker.bindPopup(this.createPopup(location));
          this.markerLayers.addLayer(marker);
        });
      }).catch((e: RequestError) => { 
        removeChildren(document.getElementById('error')); 
        const message = 'An error occurred, please try again';
        new ErrorSvelte({props: {message: message}, target: document.getElementById('error')});
        this.errorTimeout = setTimeout(() => {removeChildren(document.getElementById('error'))}, error_duration);
      });
  }

  destroy() {
    if(this.errorTimeout) clearTimeout(this.errorTimeout);
  }

  resizeMap() {
    if(this.map) this.map.invalidateSize();
  }

  refresh() {
    const bounds = this.map.getBounds();
    const zoom = this.map.getZoom();
    const center = bounds.getCenter();
    const width = bounds.getEast()-bounds.getWest();
    const height = bounds.getNorth()-bounds.getSouth();

    const currentPosition = new Position(center.lat, center.lng);

    if(!this.lastRefreshPosition || currentPosition.distance(this.lastRefreshPosition)>Math.min(width, height)/2.0 || Math.abs(zoom-this.lastRefreshZoom)>1) {
      const filter = new Filter(false, currentPosition.lat, currentPosition.long, currentPosition.lat, currentPosition.long, Math.max(width, height), 0.0);
      this.rankedList.set(ResultsModel.getInstance().getRankedList(filter));
      this.lastRefreshPosition = currentPosition;
      this.lastRefreshZoom = zoom;
    }
  }
}
