describe('calculateMonthlyPayment Tests', function(){
  it('should calculate the monthly rate correctly', function () {
      let values = {amount: 10000, years : 10, rate: 4.5}
      expect(calculateMonthlyPayment(values)).toEqual('103.64')
      values = {amount: 50000, years : 5, rate: 3}
      expect(calculateMonthlyPayment(values)).toEqual('898.43')
  })})

describe ('calculateMonthly Payment Precision Tests', function(){
  it("should return a result with 2 decimal places", function() {
    let values = {amount: 9648.93, years : 10, rate: 4.5}
    expect(calculateMonthlyPayment(values)).toEqual('100.00')
  });
});

describe('calculateMonthly Wrong Input Tests', function(){
  it('should throw an error when invalid input for principal', function(){
    let values = {amount: "hello", years : 10, rate: 4.5}
    expect(() => calculateMonthlyPayment(values)).toThrowError("Bad Input");
    values = {amount: 10000, years : "years", rate: 4.5}
    expect(() => calculateMonthlyPayment(values)).toThrowError("Bad Input");
    values = {amount: 10000, years : 10, rate: "rates"}
    expect(() => calculateMonthlyPayment(values)).toThrowError("Bad Input");
  })
})

describe('calculateMonthly Negative Input Tests', function(){
  it('should throw an error when invalid input for principal', function(){
    let values = {amount: -10000, years : 10, rate: 4.5}
    expect(() => calculateMonthlyPayment(values)).toThrowError('Negative Input');
    values = {amount: 10000, years : -10, rate: 4.5}
    expect(() => calculateMonthlyPayment(values)).toThrowError('Negative Input');
    values = {amount: 10000, years : 10, rate: -4.5}
    expect(() => calculateMonthlyPayment(values)).toThrowError('Negative Input');
  })
})
