interface Model {
    id: number;
}

export class SocialProfile implements Model {
    id: number;
    username: string;
    followers_count: number;

    constructor(id: number = 0, username: string = 'default username', followers_count: number = 0) {
        this.id = id; this.username = username; this.followers_count = followers_count;
    }
}

export class Position {
    lat: number;
    long: number;

    constructor(lat: number = 0.0, long: number = 0.0) {
        this.lat = lat; this.long = long;
    }

    distance(other: Position) {
        return Math.sqrt(Math.pow(this.lat-other.lat, 2) + Math.pow(this.long-other.long, 2));
    }
}

export class Location implements Model {
    id: number;
    name: string;
    position: Position;
    score: number | null;

    constructor(id: number = 0, name: string = 'default name', position: Position = new Position(0.0, 0.0), score: number = 0.0) {
        this.id = id; this.name = name; this.position = position; this.score = score;
    }
}

export class Account {
    idtoken: string;
    accesstoken: string;
    accountname: string;
    email: string;
    preference: boolean;

    constructor(idtoken: string, accesstoken: string, accountname: string = 'default name', email: string = 'default email', preference: boolean = true) {
        this.idtoken=idtoken; this.accesstoken=accesstoken; this.accountname = accountname; this.email=email; this.preference = preference;
    }
}

export class Info {
    name: string; 
    img: any;
    address: string;
    score: number;

    constructor(name: string, img: any, address:string, score:number) {this.name=name; this.img=img; this.address=address; this.score=score;}
}

export class Filter {
    only_from_followed: boolean;
    current_lat: number;
    current_long: number;
    radius: number;
    min_rating: number;

    constructor(only_from_followed: boolean=false, current_lat: number=null, current_long: number=null, radius: number=null, min_rating: number=0.0) {
        this.only_from_followed=only_from_followed; this.current_lat=current_lat; this.current_long=current_long; this.radius=radius; this.min_rating=min_rating;
    }
}

export class RequestError extends Error {
    code: number;
    message: string;

    constructor(code: number, message: string) {super(message); this.code=code; this.message=message;}
}