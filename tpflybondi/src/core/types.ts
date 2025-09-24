export type Flight = {
    origin: string;
    destination: string;
    price: number;
    availability: number;
    date: string; // ISO
  };
  
  export type RoundTrip = {
    origin: string;
    destination: string;
    departDate: string; // ISO
    returnDate: string; // ISO
    priceOut: number;
    priceReturn: number;
    totalPrice: number; // por persona
    nights: number;
    availOut: number;
    availReturn: number;
  };
  