import React, { useState } from 'react';
import './ProfileComponent.css';

const ProfileComponent = () => {
  const [activeSection, setActiveSection] = useState('profile');
  const [showAddAddressModal, setShowAddAddressModal] = useState(false);
  const [addressList, setAddressList] = useState([]);
  const [address, setAddress] = useState({
    name: '',
    mobile: '',
    pincode: '',
    locality: '',
    city: '',
    state: '',
    address: '',
    landmark: '',
    alternatePhone: ''
  });

  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  const handleAddAddress = () => {
    setShowAddAddressModal(true);
  };

  const handleCloseModal = () => {
    setShowAddAddressModal(false);
  };

  const handleSaveAddress = (e) => {
    e.preventDefault();
    setAddressList([...addressList, address]);
    setAddress({
      name: '',
      mobile: '',
      pincode: '',
      locality: '',
      city: '',
      state: '',
      address: '',
      landmark: '',
      alternatePhone: ''
    });
    setShowAddAddressModal(false);
  };

  return (
    <section className="profile-component my-5">
      <div className="container">
        <div className="main-body">
          <div className="row">
            {/* Left Sidebar */}
            <div className="col-lg-4">
              <div className="card">
                <div className="card-body">
                  <div className="d-flex flex-column align-items-center text-center">
                    <img 
                      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtbEsykx-0fhTred6UwHDYtMFd2UgTJCG4gaklT1dx4suRO4_n5LJr4Gg28kquSX5fpNo&usqp=CAU" 
                      alt="Admin" 
                      className="rounded-circle p-1 bg-warning profile-image"
                    />
                    <div className="mt-3">
                      <h4>Jyoti</h4>
                      <p className="text-secondary mb-1">+91 7493658737</p>
                      <p className="text-muted font-size-sm">Delhi, NCR</p>
                    </div>
                  </div>
                  <div className="list-group list-group-flush text-center mt-4">
                    <button 
                      className={`list-group-item list-group-item-action border-0 ${activeSection === 'profile' ? 'active' : ''}`}
                      onClick={() => handleSectionChange('profile')}
                    >
                      Profile Information
                    </button>
                    <button 
                      className={`list-group-item list-group-item-action border-0 ${activeSection === 'orders' ? 'active' : ''}`}
                      onClick={() => handleSectionChange('orders')}
                    >
                      Orders
                    </button>
                    <button 
                      className={`list-group-item list-group-item-action border-0 ${activeSection === 'address' ? 'active' : ''}`}
                      onClick={() => handleSectionChange('address')}
                    >
                      Address Book
                    </button>
                    <button className="list-group-item list-group-item-action border-0">
                      Logout
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Content */}
            <div className="col-lg-8">
              {/* Profile Information */}
              {activeSection === 'profile' && (
                <div className="card">
                  <div className="card-body">
                    <div className="profile-info">
                      <h5>Profile Information</h5>
                      <p><strong>Name:</strong> Jyoti</p>
                      <p><strong>Email Address:</strong> jyoti@gmail.com</p>
                      <p><strong>Contact:</strong> +91 7493658737</p>
                      <p><strong>Date of Birth:</strong> 02-03-1999</p>
                      <p><strong>Gender:</strong> Female</p>
                      <p><strong>City:</strong> Delhi, NCR</p>
                      <p><strong>Height:</strong> 5.4</p>
                      <p><strong>Weight:</strong> 50</p>
                      <p><strong>Goal:</strong> Hair & Skin</p>
                      <p><strong>Preference:</strong> Pure Vegetarian</p>
                      <p><strong>Role:</strong> User</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Order Details */}
              {activeSection === 'orders' && (
                <div className="order-card">
                  {/* Order details content from original HTML */}
                </div>
              )}

              {/* Address Book */}
              {activeSection === 'address' && (
                <div className="card">
                  <div className="card-body">
                    <h5>Address Book</h5>
                    <button className="add-address-button" onClick={handleAddAddress}>
                      Add Address
                    </button>
                    
                    <div className="address-list">
                      {addressList.map((addr, index) => (
                        <div key={index} className="address-item">
                          <p>{addr.name}</p>
                          <p>{addr.address}</p>
                          <p>{addr.city}, {addr.state} - {addr.pincode}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Add Address Modal */}
              {showAddAddressModal && (
                <div className="address-modal">
                  <div className="modal-content">
                    <span className="close-button" onClick={handleCloseModal}>&times;</span>
                    <h2>Add Address</h2>
                    <form onSubmit={handleSaveAddress}>
                      {/* Form fields from original HTML */}
                    </form>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProfileComponent;



.profile-component .list-group-item.active {
    background: #06C167 !important;
    color: white;
}

.profile-component .bg-warning {
    background: #06C167 !important;
}

.profile-component .profile-image {
    width: 110px;
    height: 110px;
    border: 2px solid #06C167;
}

.profile-component .top-status ul {
    list-style: none;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    padding: 0;
    margin: 0;
}

.profile-component .top-status ul li {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: #fff;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    border: 8px solid #ddd;
    box-shadow: 1px 1px 10px 1px #ddd inset;
    margin: 10px 5px;
}

.profile-component .top-status ul li.active {
    border-color: #06C167;
    box-shadow: 1px 1px 20px 1px #ffc107 inset;
}

.profile-component .timeline {
    list-style-type: none;
    position: relative;
    padding-left: 0;
}

.profile-component .timeline:before {
    content: ' ';
    background: #d4d9df;
    display: inline-block;
    position: absolute;
    left: 29px;
    width: 2px;
    height: 100%;
    z-index: 400;
}

.profile-component .timeline > li {
    margin: 20px 0;
    padding-left: 30px;
}

.profile-component .timeline > li:before {
    content: '\2713';
    background: #fff;
    display: inline-block;
    position: absolute;
    border-radius: 50%;
    border: 0;
    left: 5px;
    width: 50px;
    height: 50px;
    z-index: 400;
    text-align: center;
    line-height: 50px;
    color: #d4d9df;
    font-size: 24px;
    border: 2px solid #06C167;
}

.profile-component .timeline > li.active:before {
    background: #28a745;
    color: #fff;
}

.profile-component .add-address-button {
    background: #06C167;
    border: 1px solid #06C167;
    padding: 8px 20px;
    color: white;
    border-radius: 4px;
    margin-bottom: 20px;
}

.profile-component .address-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.profile-component .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 70%;
    max-width: 600px;
}

.profile-component .close-button {
    float: right;
    font-size: 24px;
    cursor: pointer;
}

@media (max-width: 768px) {
    .profile-component .main-flex-div {
        flex-direction: column;
    }
    
    .profile-component .inner-flex-div {
        width: 100% !important;
        margin-bottom: 15px;
    }
    
    .profile-component .modal-content {
        width: 95%;
        padding: 15px;
    }
}
